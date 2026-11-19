function result = analyze_engine_audio(filename)
%ANALYZE_ENGINE_AUDIO Descriptive DSP analysis of one engine WAV recording.
%   This is an educational feature comparison, not a fault classifier.
%   MFCC summaries are returned only when the Audio Toolbox mfcc function
%   is available in the MATLAB installation.

    arguments
        filename (1,1) string
    end
    if ~isfile(filename)
        error('engine_dsp:FileNotFound', 'Audio file not found: %s', filename);
    end

    [audio, sampleRate] = audioread(filename);
    if isempty(audio) || sampleRate <= 0
        error('engine_dsp:InvalidAudio', 'Audio is empty or has an invalid sample rate.');
    end
    mono = mean(audio, 2);
    if any(~isfinite(mono))
        error('engine_dsp:InvalidAudio', 'Audio contains NaN or infinite samples.');
    end

    n = numel(mono);
    windowed = mono .* hann(n, 'periodic');
    spectrum = abs(fft(windowed));
    spectrum = spectrum(1:floor(n/2)+1);
    if numel(spectrum) > 2
        spectrum(2:end-1) = 2 .* spectrum(2:end-1);
    end
    frequency = (0:numel(spectrum)-1)' .* sampleRate ./ n;
    spectrum(1) = 0; % exclude DC from spectral descriptors
    magnitudeSum = sum(spectrum);

    features = struct();
    features.rms = sqrt(mean(mono.^2));
    if n > 1
        features.zero_crossing_rate = mean(diff(mono >= 0) ~= 0);
    else
        features.zero_crossing_rate = 0;
    end
    if magnitudeSum > 0
        centroid = sum(frequency .* spectrum) ./ magnitudeSum;
        features.spectral_centroid_hz = centroid;
        features.spectral_bandwidth_hz = sqrt(sum(((frequency-centroid).^2).*spectrum)./magnitudeSum);
        cumulativePower = cumsum(spectrum.^2);
        index = find(cumulativePower >= 0.85*cumulativePower(end), 1, 'first');
        features.spectral_rolloff_85_hz = frequency(index);
        [~, peakIndex] = max(spectrum);
        features.dominant_frequency_hz = frequency(peakIndex);
    else
        features.spectral_centroid_hz = 0;
        features.spectral_bandwidth_hz = 0;
        features.spectral_rolloff_85_hz = 0;
        features.dominant_frequency_hz = 0;
    end

    if exist('mfcc', 'file') == 2
        coefficients = mfcc(mono, sampleRate, 'NumCoeffs', 13);
        features.mfcc_mean = mean(coefficients, 1);
        features.mfcc_std = std(coefficients, 0, 1);
    else
        features.mfcc_mean = [];
        features.mfcc_std = [];
        warning('engine_dsp:NoMFCC', 'Audio Toolbox mfcc function unavailable; MFCC summaries omitted.');
    end

    result = struct('file', filename, 'sample_rate_hz', sampleRate, ...
                    'features', features, 'spectrum_frequency_hz', frequency, ...
                    'spectrum_magnitude', spectrum);
end
