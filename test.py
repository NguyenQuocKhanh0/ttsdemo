def check_len_text(text):
    num_of_char = 500
    temp = text
    count = 0 
    i = 0
    split_text = []
    while count+num_of_char < len(text):
        x = temp[count:count+num_of_char].rindex(".")
        split_text.append(temp[count:count+x+1])
        #print('------------------------------------')
        count = count + x + 1
        i +=1
    left = temp[count:len(text)]
    split_text.append(left)
    print(len(split_text))
    for text in split_text:
        print(text)
        print(len(text))
        print('--------------')
    return split_text

# text = 'Trước khi Thế vận hội khai mạc, nhiều nhà khoa học đã cảnh báo Olympic có thể tạo ra các ổ dịch lớn làm lây lan virus ra cộng đồng dân cư nói chung. Đây là rủi ro luôn đi kèm khi tổ chức các sự kiện quốc tế lớn giữa đại dịch. Nhưng thực tế cho thấy, Nhật Bản dường như đã kiểm soát tốt tình hình. Các vận động viên và quan chức thể thao nước ngoài đến Nhật Bản từ tháng trước được yêu cầu xét nghiệm Covid-19 hai lần trong vòng 96 tiếng trước khi chuyến bay của họ khởi hành, tiếp tục xét nghiệm thêm một lần nữa khi tới nơi và cách ly trong ba ngày đầu. Vận động viên phải xét nghiệm hàng ngày trong thời gian ở Nhật Bản và rời đi trong 48 tiếng sau khi môn thi của họ kết thúc. tiếp tục xét nghiệm thêm một lần nữa khi tới nơi và cách ly trong ba ngày đầu. Vận động viên phải xét nghiệm hàng ngày trong thời gian ở Nhật Bản và rời đi trong 48 tiếng sau khi môn thi của họ kết thúc. tiếp tục xét nghiệm thêm một lần nữa khi tới nơi và cách ly trong ba ngày đầu. Vận động viên phải xét nghiệm hàng ngày trong thời gian ở Nhật Bản và rời đi trong 48 tiếng sau khi môn thi của họ kết thúc.'
# print(text, len(text))
# split_text = check_len_text(text)

from pydub import AudioSegment
audio_list = ['/home/son/Downloads/hhp/text_to_speech_hhp/output/2021_08_12_15_28_49_0.wav','/home/son/Downloads/hhp/text_to_speech_hhp/output/2021_08_12_15_28_49_1.wav', '/home/son/Downloads/hhp/text_to_speech_hhp/output/2021_08_12_15_28_49_2.wav'] 

wavs = [AudioSegment.from_wav(wav) for wav in audio_list]
combined = (wavs[0])
file_path = '/home/son/Downloads/hhp/text_to_speech_hhp/output/2021_08_12_15_28_49.wav'
for wav in wavs[1:]:
    combined = combined.append(wav)
combined.export(file_path, format="wav", parameters=["-ar", "16000"])