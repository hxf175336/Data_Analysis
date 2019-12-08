import mysql.connector
from scipy.io.wavfile import read
import pyaudio
import numpy as np
import wave
import datetime
from scipy import signal
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure,iterate_structure, binary_erosion)
import hashlib
from operator import itemgetter
from numpy import cos, sin, pi, absolute, arange
from scipy.signal import lfilter, firwin, freqz
from pylab import figure, clf, plot, xlabel, ylabel, xlim, ylim, title, grid, axes, show


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="123456",
  database="FingerprintingDatabase"
)

def saveFingerprint(ambiente,hash_list,nome):
    mycursor = mydb.cursor()

    sql = "SELECT id_ambiente FROM ambientes WHERE descricao='"+ambiente+"'"
    mycursor.execute(sql)
    ambienteId = mycursor.fetchone()[0]
    print("ID ambiente: ",ambienteId)

    #sql = "INSERT INTO registos (id_ambiente,nome) VALUES ("+str(ambienteId)+","+str(nome)+")"
    #mycursor.execute(sql)
    sql = "INSERT INTO registos (id_ambiente,nome) VALUES (%s,%s)"
    val = (ambienteId,nome)
    mycursor.execute(sql, val)
    mydb.commit()

    sql = "SELECT id FROM registos ORDER BY id DESC LIMIT 1"
    mycursor.execute(sql)
    myresult = mycursor.fetchone()[0]
    print("Last insert: ",myresult)

    for i in range(0,len(hash_list)):
        sql = "INSERT INTO fingerprint (sha1_hash, time_offset, registo_id) VALUES (%s,%s,%s)"
        val = (hash_list[i][0],int(hash_list[i][1]),myresult)
        mycursor.execute(sql, val)
        mydb.commit()

def getFingerprint(id):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT sha1_hash FROM fingerprint WHERE registo_id="+str(id))
    myresult = mycursor.fetchall()
    return myresult

def getAllRegisters():
    mycursor = mydb.cursor()

    sql = "SELECT ambientes.descricao,registos.nome,registos.id " \
          "FROM registos " \
          "INNER JOIN ambientes ON registos.id_ambiente = ambientes.id_ambiente\
          ORDER BY ambientes.descricao;"

    mycursor.execute(sql)
    result = mycursor.fetchall()
    return result

def getSoundSample():
    p = pyaudio.PyAudio()

    pyaudio_format = pyaudio.paInt16
    now_ts = datetime.datetime.now()
    now_ts_str = now_ts.strftime("%Y-%m-%d_%H-%M-%S")
    print('Current Timestamp : ', now_ts_str)
    WAVE_OUTPUT_FILENAME = "audioFiles/"+now_ts_str + ".wav"

    stream = p.open(format=pyaudio_format, channels=n_channels, rate=samplerate, input=True,
                    frames_per_buffer=buffer_size)
    frames = []
    print("recording...")

    for i in range(0, int(samplerate / buffer_size * record_sec)):
        data = stream.read(buffer_size)
        frames.append(data)
    print("finished recording")

    # stop Recording\n",
    stream.stop_stream()
    stream.close()
    p.terminate()

    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(n_channels)
    waveFile.setsampwidth(p.get_sample_size(pyaudio_format))
    waveFile.setframerate(samplerate)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()
    return WAVE_OUTPUT_FILENAME

def readAudioFile(filename):
    samplerate, audio = read(filename)
    plt.plot(audio)
    plt.show()
    return samplerate, audio

def calculateSpectrogram(audio):
    plt.rcParams['figure.figsize'] = 16, 4
    index_limit = int(freq_limit // frequency_res)
    print(frequency_res, index_limit)

    print(segment_length, segment_overlap)

    f, t, S = signal.spectrogram(audio, samplerate, window='flattop', nperseg=segment_length, noverlap=segment_overlap,
                                 scaling='spectrum', mode='magnitude')

    print('Data length (s): ', t[-1])
    print('Sampling frequency (samples/s): ', samplerate)
    plt.pcolormesh(t, f[:index_limit], S[:index_limit][:])
    plt.xlabel('time(s)')
    plt.ylabel('frequency(Hz)')
    plt.show()
    return f, t, S

def extractEnergyPeaks(f, t, S):
    specgram = S[:index_limit][:]
    PEAK_NEIGHBORHOOD_SIZE = 2  # Number of cells around an amplitude peak in the spectrogram in order to be considered a spectral peak.

    def get_2D_peaks(arr2d, amp_min=threshold):
        # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
        struct = generate_binary_structure(2, 1)
        neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

        # find local maxima using our fliter shape
        local_max = maximum_filter(arr2d, footprint=neighborhood) == arr2d
        background = (arr2d <= 40.0)
        eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

        # Boolean mask of specgram with True at peaks
        detected_peaks = 1 * local_max - 1 * eroded_background

        # extract peaks
        amps = arr2d[detected_peaks]
        j, i = np.where(detected_peaks)

        # filter peaks by amplitude
        amps = amps.flatten()
        peaks = zip(i, j, amps)  # freq, time, amp

        peaks_filtered = []
        for x in peaks:
            if x[2] > amp_min:
                peaks_filtered.append(x)
            else:
                detected_peaks[x[1]][x[0]] = False

        # get indices for frequency and time
        frequency_idx = [x[1] for x in peaks_filtered]
        time_idx = [x[0] for x in peaks_filtered]

        return zip(frequency_idx, time_idx), detected_peaks

    local_maxima, bin_spec = get_2D_peaks(specgram, amp_min=threshold)
    local_max_list = list(local_maxima)

    plt.pcolormesh(bin_spec)
    plt.xlabel('time(s)')
    plt.ylabel('frequency(Hz)')
    plt.show()
    return local_max_list

def generate_hashes(peaks, fan_value):
    """
    Hash list structure:
       sha1_hash[0:20]    time_offset
    [(e05b341a9b77a51fd26, 32), ... ]
    """
    peaks.sort(key=itemgetter(1))  # sort peaks temporally for fingerprinting

    # Thresholds on how close or far fingerprints can be in time in order
    # to be paired as a fingerprint
    MIN_HASH_TIME_DELTA = 0
    MAX_HASH_TIME_DELTA = 200

    # Number of bits to throw away from the front of the SHA1 hash in the
    # fingerprint calculation. The more you throw away, the less storage, but
    # potentially higher collisions and misclassifications when identifying songs.
    FINGERPRINT_REDUCTION = 20  # SHA-1 has 40 digits maximum

    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                freq1 = peaks[i][0]
                freq2 = peaks[i + j][0]
                t1 = peaks[i][1]
                t2 = peaks[i + j][1]
                t_delta = t2 - t1

                if t_delta >= MIN_HASH_TIME_DELTA and t_delta <= MAX_HASH_TIME_DELTA:
                    str_to_hash = "%s|%s|%s" % (str(freq1), str(freq2), str(t_delta))
                    h = hashlib.sha1(str_to_hash.encode('utf-8'))
                    yield (h.hexdigest()[0:FINGERPRINT_REDUCTION], t1)

def calcularRelacao(lista1,lista2):
    count=0
    for i in range(len(lista1)):
        for j in range(len(lista2)):
            if lista1[i][0] == lista2[j][0]:
                count+=1
    return count/len(lista1),count

def filtroLowPass(audio,cutoff_hz,ordem):
    nyq_rate = samplerate / 2.0
    taps = firwin(ordem, cutoff_hz / nyq_rate)  # b coefficients = taps
    filtered_audio = lfilter(taps, 1.0, audio)
    plt.plot(audio)
    plt.show()
    return filtered_audio

if __name__ == '__main__':
    threshold = 70.0  # Minimum amplitude in spectrogram in order to be considered a peak.
    buffer_size = 4096
    n_channels = 1
    record_sec = 5
    samplerate = 48000
    buffer_size = 4096
    freq_limit = 1000  # in Hz
    segment_length = samplerate // 2
    segment_overlap = samplerate // 4
    frequency_res = samplerate / segment_length
    index_limit = int(freq_limit // frequency_res)

    #waveOutputFilename = getSoundSample()
    samplerate, audio = readAudioFile('audioFiles/Teste/RightRoundTeste_2.wav')
    f, t, S = calculateSpectrogram(audio)
    local_max_list=extractEnergyPeaks(f, t, S)
    hashes = generate_hashes(peaks=local_max_list, fan_value=5)
    hash_list = list(hashes)
    #saveFingerprint('Hip Hop',hash_list,'Right Round')


    amostra = hash_list
    listaTiposAudio = getAllRegisters()

    resultadosMatching=[]
    for tipoAudio in listaTiposAudio:
        fingerPrint = getFingerprint(tipoAudio[2])
        resultado = calcularRelacao(amostra, fingerPrint)
        thistuple = tuple((tipoAudio[0],tipoAudio[1],resultado[0],resultado[1]))
        resultadosMatching.append(thistuple)

    max=resultadosMatching[1]

    for resultado in resultadosMatching:
        print(resultado)
        if resultado[2]>max[2]:
            max=resultado
    print("\n\nMax :",max)


