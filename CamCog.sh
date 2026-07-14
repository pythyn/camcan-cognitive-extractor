#!/bin/bash

# Execute CamCog data extraction
python CamCog.py \
    --base "/home/amyr/Datasets/raw/camcan01869/cc700-scored" \
    --test "BentonFaces" --cols TotalScore \
    --test "Cattell" --cols TotalScore \
    --test "EkmanEmHex" --cols Acc \
    --test "EmotionalMemory" --cols TotNamed \
    --test "EmotionRegulation" --cols NeuW_mean_WvsR \
    --test "FamousFaces" --cols FAMnam \
    --test "ForceMatching" --cols FingerOverCompensationMean \
    --test "Hotel" --cols Time \
    --test "MotorLearning" --cols LateExposureTrajectoryErrorMean \
    --test "MRI" --cols PctCorrect,mRT,mdnRT,stdRT,cvRT \
    --test "PicturePriming" --cols pfx_reITRT_corrp_low_sem \
    --test "Proverbs" --cols Score \
    --test "RTchoice" --cols PctCorrect_all,RTtrim3mean_all \
    --test "RTsimple" --cols PctCorrect,RTtrim3mean \
    --test "Synsem" --cols synsub_reITRT_mean \
    --test "TOT" --cols ToT_ratio \
    --test "VSTMcolour" --cols K_ss4 \
    --sub "./sub.txt" \
    --output merged.csv
