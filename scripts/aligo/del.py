import os

del_list = ['2021\diushi\lv_0_20210530183212(1).mp4'
            ,'2021\锻炼record\VID_20200517_205915(0).mp4',
            '2020\Camera\VID_20200517_205915(0).mp4',
            '2021\diushi\lv_0_20210530183212.mp4',
            '2021\diushi\lv_6853735523966553344_20211228023122.mp4',
            '2020\Camera\2048e168eca20413ecaf16ecf385f586.jpg',
            '2020\Camera\VID_20200321_164003.mp4',
            "2020\Camera\temp_uuid_e35c6a00d74cb5dbe7ed469282fd7183.mp4"
            ]
p = ""
for e in del_list:
    os.remove(os.path.join(p, e))