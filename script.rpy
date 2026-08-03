# =================================----------------===
# 1. 키맵 설정 및 매너 모드 기능
# =================================----------------===
init 999 python:
    # 기존 스킵 관련 키맵(skip, toggle_skip, fast_skip)에서 Tab 키 완전히 제거
    for skip_action in ['skip', 'toggle_skip', 'fast_skip']:
        if skip_action in config.keymap:
            config.keymap[skip_action] = [k for k in config.keymap[skip_action] if k not in ('K_TAB', 'tab')]

    # 매너 모드 전용 키로 Tab 등록
    config.keymap['toggle_manner_mode'] = ['K_TAB']

    # 매너 모드 토글 함수
    def toggle_manner():
        if renpy.get_screen("manner_overlay"):
            renpy.hide_screen("manner_overlay")
            for ch in ['music', 'sound', 'voice', 'ambient']:
                try:
                    renpy.music.set_pause(False, channel=ch)
                except Exception:
                    pass
        else:
            for ch in ['music', 'sound', 'voice', 'ambient']:
                try:
                    renpy.music.set_pause(True, channel=ch)
                except Exception:
                    pass
            renpy.show_screen("manner_overlay")
        renpy.restart_interaction()

    # 오버레이 스크린 상시 등록
    if "manner_key_listener" not in config.overlay_screens:
        config.overlay_screens.append("manner_key_listener")

    # 스팀 오버레이로 상점/찜하기 페이지를 강제로 띄우는 파이썬 함수
    def open_steam_store_overlay(app_id="5036480"):
        try:
            import steamworks
            if steamworks.is_steam_running():
                steamworks.Friends.ActivateGameOverlayToStore(int(app_id), 0)
            else:
                renpy.open_url("https://store.steampowered.com/app/" + str(app_id))
        except Exception:
            renpy.open_url("https://store.steampowered.com/app/" + str(app_id))

# 키 입력 감지 스크린 (기본 화면용)
screen manner_key_listener():
    key "toggle_manner_mode" action Function(toggle_manner)

# 매너 모드 덮개 스크린 (덮개 활성화 상태용)
screen manner_overlay():
    modal True
    zorder 99999
    key "toggle_manner_mode" action Function(toggle_manner)
    add "#000000"
    vbox:
        align (0.5, 0.5)
        spacing 15
        text "MANNER MODE ACTIVE" color "#ffffff" size 36 bold True align (0.5, 0.5)
        text "Press Tab / Paddle to Resume" color "#888888" size 20 align (0.5, 0.5)

# =================================----------------===
# [0] 오디오 채널 및 자동 감지 로직 설정
# =================================----------------===
init python:
    # 빗소리 등 배경 환경음 전용 채널
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)

    # 실제 오디오 파일 위치를 자동으로 감지하는 함수
    def find_audio(filename):
        candidates = [
            "audio/sfx/" + filename,
            "audio/bgm/" + filename,
            "audio/" + filename,
            "sfx/" + filename,
            "bgm/" + filename,
            filename
        ]
        for path in candidates:
            if renpy.loadable(path):
                return path
        return filename

# 사운드 기능 활성화 및 기본 볼륨 설정
define config.has_sound = True
default preferences.sfx_volume = 1.0

# BGM 오디오 경로 자동 탐색 매핑
define audio.bgm_main = find_audio("bgm.mp3")
define audio.bgm_daily = find_audio("bgm1.mp3")
define audio.bgm_sad = find_audio("bgm2.mp3")
define audio.bgm_wafu = find_audio("bgm3.mp3")

# SFX 오디오 경로 자동 탐색 매핑
define audio.sfx_door = find_audio("sfx_door.mp3")
define audio.sfx_bell = find_audio("sfx_bell.mp3")
define audio.sfx_hit = find_audio("sfx_hit.mp3")
define audio.sfx_crash = find_audio("sfx_crash.mp3")
define audio.sfx_magic = find_audio("sfx_magic.mp3")

# =================================----------------===
# 캐릭터 정의
# =================================----------------===
define h = Character('서로아', color="#FF4D4D")
define m = Character('연하랑', color="#c8ffc8")
define j = Character('연하진', color="#8c9eff")
define y = Character('여대생(유나)', color="#E0E0E0")
define g = Character('가주', color="#A0A0A0")

# =================================----------------===
# 이미지 에셋 및 트랜스폼 정의
# =================================----------------===

# --- 배경 이미지 ---
image bg_room_day = "images/bg/home.jpg"
image bg_room_sunset = Transform("images/bg/home.jpg", matrixcolor=TintMatrix("#ffccaa") * BrightnessMatrix(-0.15))
image bg_room_night = Transform("images/bg/home.jpg", matrixcolor=TintMatrix("#4c607a") * BrightnessMatrix(-0.35))
image bg_store_day = "images/bg/bg23_01.jpg"
image bg_store_night = Transform("images/bg/bg23_01.jpg", matrixcolor=TintMatrix("#4c607a") * BrightnessMatrix(-0.35))
# 달빛 편의점 면접 씬 (bg24_01.jpg 에셋 + 새벽 낡은 편의점 연출)
image bg_store_interview = Transform("images/bg/bg24_01.jpg", matrixcolor=TintMatrix("#4c607a") * BrightnessMatrix(-0.30))
image bg_street_night = Solid("#2c3e50")

# --- 캐릭터 스탠딩 이미지 (zoom=0.35, yalign=1.0) ---
image hajin normal = Transform("images/character/10_suit_normal.png", zoom=0.35, yalign=1.0)
image hajin angry = Transform("images/character/10_suit_angry.png", zoom=0.35, yalign=1.0)

image roa normal = Transform("images/character/roa_normal.png", zoom=0.35, yalign=1.0)
image roa smile = Transform("images/character/roa_smile.png", zoom=0.35, yalign=1.0)
image roa sad = Transform("images/character/roa_sad.png", zoom=0.35, yalign=1.0)
image roa blush = Transform("images/character/roa_blush.png", zoom=0.35, yalign=1.0)
image roa angry = Transform("images/character/roa_angry.png", zoom=0.35, yalign=1.0)

# =================================----------------===
# 메인 스토리 - 프롤로그 및 첫 만남
# =================================----------------===

label start:
    scene black with fade
    play music bgm_main fadein 1.0

    "이 세상에는 인간의 탈을 쓰고 함께 살아가는 요괴와 악마들이 존재한다."
    "현대 사회에서 뿔이나 꼬리 같은 특징을 드러내고 다닐 수는 없는 노릇."
    "따라서 영물들이나 퇴마사, 악마들까지도 이형의 특징을 마력으로 완벽히 숨긴다."
    "진짜 모습은 마력이 극도로 요동치거나 방심할 때만 드러날 뿐이다."
    "…적어도 내가 가문에서 배운 상식은 그랬다."

    scene bg_room_night with fade
    play sound sfx_door

    m "으아하....오늘 하루도 진짜 영혼까지 털렸네."
    m "퇴마사 가문에서 제발로 나왔을 땐 부자가 될 줄 알았지."
    m "현실은 통장 잔고 1,400원에 컵라면도 감지덕지라니..."

    "터덜터덜 현관문을 열고 자취방으로 들어섰다. 그런데..."

    m "...어?"

    "방 한구석, 내가 아끼는 소파 위에 누군가 누워있다."
    
    show roa normal at center with dissolve
    "길고 새까만 흑발, 끝부분만 살짝 붉은 머리칼... 머리 위 뿔과 뒤에 보이는 악마 꼬리?!"

    play sound sfx_hit
    m "악마... 악마 꼬리?!"
    m "인간계에 올라왔으면 뿔이랑 꼬리는 숨기는 게 기본 상식 아닙니까?!"

    show roa smile
    h "음냐... 하랑아, 왔어? 오늘 퇴마 일거리는 좀 들어왔니?"

    m "누, 누구세요?! 내 방엔 어떻게 들어왔고, 내 이름은 또 어떻게 아는데?!"

    show roa sad
    h "아하하, 박대하지 마~ 나 정기 부족해서 뿔이랑 꼬리를 숨길 마력도 없단 말이야."
    h "이대로 쫓아내면 나 진짜 길거리에서 바싹 말라 죽어!"

    m "아니, 저는 쫓겨난 '여우 퇴마사'거든요? 악마를 잡아서 협회에 넘겨야 한다고요!"

    show roa normal
    h "흐응... 과연 잔고 1,400원짜리 퇴마사 도련님이 나를 잡을 수 있을까?"
    
    show roa smile
    h "대신 얹혀살게 해주면 청소도 하고 맛있는 것도 해줄게! 정기 아주 조금씩만 나눠주면 안 돼?"

    m "하... 어이가 없어서 원. 좋습니다. 단, 몇 가지 규칙이 있습니다."
    m "첫째, 제 허락 없이 정기 금지. 둘째, 집안일은 반반. 셋째..."

    h "셋째는 뭔데?"

    m "제 소파에서 당장 내려오세요. 거긴 제 자리입니다."

    show roa angry
    h "치... 째째하게 굴긴!"

    show roa sad
    "서로아는 내 일침에 결국 풀이 죽어 소파에서 내려왔다."

    "접이식 식탁 위에는 김이 모락모락 피어오르는 600원짜리 컵라면 두 개가 놓였다."
    "로아는 아무 말 없이 라면 용기를 양손으로 조심스레 감싸 쥐었다."

    show roa smile
    h "...따뜻해."
    h "가장 춥고 외로울 때, 나를 쫓아내지 않아 줘서 고마워, 하랑아."

    m "...다 불어 터집니다. 쓸데없는 소리 말고 먹기나 하세요."

    "창밖으로는 밤바람 소리가 들렸지만, 어쩐지 이 좁은 방이 아주 조금 덜 춥게 느껴졌다."

    m "자, 소파는 제겁니다."

    show roa angry
    h "에에?! 바닥에서 자면 뿔이랑 꼬리 배겨서 아프단 말이야!"

    m "무단 침입한 불청객한테 제 안식처를 양보할 생각은 없습니다."

    "투덜거리는 로아를 보며 한숨을 내쉬곤, 장롱에서 푹신한 솜이불과 베개를 꺼내 던져주었다."

    show roa normal
    h "앗, 이게 뭐야?"
    m "이불이라도 덮고 자세요. 바닥 차가우니까."

    show roa smile
    h "헤헤... 뭐야, 하랑이 의외로 다정하잖아?"

    "딸깍-"
    hide roa with dissolve
    "불을 끄자 기분 좋은 어둠이 찾아왔다."

    h "...하랑아. 잘 자."
    m "...그쪽도 잘 자요."

    jump chapter_2_job_search

# =================================----------------===
# 알바 구하기 및 합격
# =================================----------------===

label chapter_2_job_search:
    scene bg_room_day with fade
    play music bgm_daily fadein 1.0

    "창문 틈 햇살과 함께 아침을 맞았다. 가슴 부근이 묵직했다."

    show roa normal at center with dissolve
    h "음냐... 하랑아, 5분만 더..."

    "양보해 준 솜이불을 껴안고 내 소파 밑 바닥에 껌딱지처럼 붙어 자는 악마. 꼬리가 내 얼굴 옆에 올려져 있었다."

    m "이봐요, 일어나세요. 해 떴습니다."
    
    show roa blush
    h "으응... 뿔 건드리지 마... 간지러워..."

    show roa smile
    h "아하암~! 잘 잤다! 인간계 이불은 진짜 따뜻하네!"

    m "통장 잔고 1,400원입니다. 오늘 단기 알바라도 안 구하면 저녁은 굶어야 해요."
    
    show roa angry
    h "에에?! 굶는 건 안 돼! 고기 먹고 싶단 말이야!"

    m "동네 알바를 찾아볼 테니 집 잘 보고 계세요."
    
    show roa smile
    h "나도 갈래! 혼자 보내면 사람 무섭다고 울면서 돌아올 것 같아!"

    "뜨끔했다. 모르는 사람과 엮이는 것 자체가 나한테는 퇴마보다 무서운 일이었으니까."

    h "같이 가! 뿔이랑 꼬리 확실히 숨기고 있을게!"

    hide roa with dissolve

    # 달빛 편의점 면접 씬 (bg24_01.jpg 에셋 + 새벽 낡은 편의점 연출)
    scene bg_store_interview with fade

    "골목길 낡은 '달빛 편의점' 창문에 야간 알바 구함 종이가 붙어 있었다."

    m "(하아... 할 수 있다. 그냥 들어가서 이력서만 드리고 나오면 돼...)"

    "손잡이를 잡은 손이 미세하게 떨렸다."
    "누군가에게 나라는 존재를 보여주고 평가받아야 한다는 건, 가문에서 매를 맞던 것만큼이나 무서운 일이었다."

    show roa smile at right with dissolve
    h "하랑아, 파이팅! 문 밖에서 내가 기운 팍팍 보내고 있을게!"

    "창밖에서 로아가 몸을 살랑이며 이상한 춤으로 응원하고 있었다."
    m "...푸흡. 다녀올게요."
    hide roa with dissolve

    play sound sfx_bell
    "딸랑-"

    "카운터에는 피곤한 기색이 역력한 점장님이 앉아계셨다."
    "나는 침을 꼴깍 삼키며, 품속에서 조심스레 이력서를 꺼내 내밀었다."

    m "저... 야간 알바 공고 보고 왔습니다."

    scene bg_room_day with fade
    "이틀이라는 시간이 흘렀다. 연락은 오지 않았다."

    show roa sad at center with dissolve
    h "하랑아... 핸드폰 구멍 뚫리겠다."

    m "이틀이나 지난 걸 보면 떨어진 게 확실합니다."

    play sound sfx_hit
    "지잉-! 지잉-!"
    "[[달빛편의점: 개인 사정으로 연락이 늦었네요. 오늘 밤 10시부터 야간 출근 가능하신가요?]"

    m "합... 합격이래요! 오늘 밤 당장 출근하래요!"
    
    show roa smile
    h "와아아아! 됐다! 합격이다! 우리 하랑이 최고!"

    hide roa with dissolve
    scene bg_room_night with fade

    show roa sad at center with dissolve
    h "하랑아, 밤길에 나쁜 귀신 나오면 어떡해?"
    
    m "퇴마사한테 귀신 걱정을 해주는 악마는 그쪽밖에 없을 겁니다. 잘 다녀올게요."

    hide roa with dissolve
    jump chapter_3_night_shift

# =================================----------------===
# 첫 야간 알바 & 정기 스릴
# =================================----------------===

label chapter_3_night_shift:
    scene bg_store_night with fade
    play music bgm_main fadein 1.0

    "새벽 3시 20분. 적막한 편의점은 세상과 단절된 나만의 작은 섬처럼 느껴졌다."

    play sound sfx_bell
    "딸랑-!"

    "커다란 후드티 모자를 눌러쓴 수상한 체구. 후드티 뒤쪽이 봉긋하게 솟아있었다."

    show roa normal at center with dissolve
    h "저... 알바생분... 혹시 저 기억나시나요...?"

    m "하... 로아 씨. 여기서 뭐 하세요?"
    
    show roa smile
    h "짠! 내가 하랑이 야식 챙겨왔지!"

    "온수통과 찌개면 컵라면. 로아는 눈을 반짝였고, 우리는 나란히 앉아 라면을 먹었다."

    m "고마워요. 로아 씨 덕분에 시간은 잘 갔네요."

    "응답이 없었다. 로아의 눈동자가 자줏빛으로 빛나고 있었다."

    show roa blush
    h "하랑아..."

    play sound sfx_magic
    "달콤한 향기가 카운터 안을 채웠다. 로아가 내 가슴팍 위로 올라탔다."

    h "정기... 피어오르고 있어... 조금만 먹을게..."

    "로아의 붉은 꼬리가 내 허벅지를 스르륵 감싸쥐었다."
    "하지만 떨리는 손끝... 본능에 지배당하면서도 날 해치지 않으려 필사적으로 참는 로아."

    m "웩! 규칙 1번 잊었습니까?"

    play sound sfx_hit
    "딱-!"
    "손가락으로 로아의 이마를 가볍게 튕겼다."

    show roa angry
    h "아얏?!"

    show roa blush
    h "하랑아! 나, 내가 방금 무슨...!"

    show roa sad
    h "미안해! 일부러 그런 거 아니야! 쫓아내지 마..."

    m "...안 쫓아냅니다. 집에서 끓여주는 정식 찌개나 먹죠. 정기는 나중에 허락할 때 줄 테니까."

    show roa smile
    h "...응! 약속할게!"

    hide roa with dissolve
    scene bg_street_night with fade

    show roa sad at center with dissolve
    m "길 잃어버리지 말고 잘 따라오세요."
    
    show roa smile
    h "어...? 헤헤, 응!"

    "손가락을 감싸 쥐는 따뜻한 체온. 아침 햇살이 다정하게 느껴졌다."

    hide roa with dissolve
    jump chapter_4_behind_friday

# =================================----------------===
# [6] 주말 일상 & 노란 베개 선물
# =================================----------------===

label chapter_4_behind_friday:
    scene bg_room_day with fade

    show roa sad at center with dissolve
    h "하랑아... 나 어제 진짜 미안했어..."

    m "로아 씨, 이쪽으로 와봐요."
    
    show roa blush
    "손이 이렇게 차가운데 참느라 고생했습니다. 조금 나누어 줄게요."

    "로아의 손을 잡고 맑은 양기를 모았다."

    h "따뜻해... 너무 맑아..."

    play sound sfx_magic
    "로아의 꼬리가 내 허리를 부드럽게 감싸 안았다."

    m "...여기까지. 약속은 약속입니다."

    show roa smile
    h "와아! 기운이 펄펄 나! 평생 너한테 잘할게!"

    hide roa with dissolve
    jump chapter_5_weekend_cooking

label chapter_5_weekend_cooking:
    scene bg_room_sunset with fade
    play music bgm_daily fadein 1.0

    "보글보글- 부엌에서 로아가 앞치마를 두르고 찌개를 끓이고 있었다."

    show roa smile at center with dissolve
    h "짠! 아침에 하랑이가 준 돈에서 만 원만 빼서 돼지고기 김치찌개 끓였어!"

    "숟가락을 들었다. 목구멍을 넘어가는 뜨끈한 국물에 얼어붙은 마음이 녹아내렸다."

    m "...맛있네요. 최근 몇 년간 먹은 것 중 제일입니다."

    h "다행이다! 많이 먹어!"

    m "밥값은 했으니 이제 생활용품 사러 가죠. 칫솔도 사고요."

    hide roa with dissolve
    jump chapter_6_shopping_spree

label chapter_6_shopping_spree:
    scene bg_store_day with fade

    show roa smile at center with dissolve
    h "짠! 빨간색 칫솔이랑 연두색 커플 칫솔로 쓰자!"

    "수면 코너를 지나다 1만 원짜리 노란색 둥근 베개를 장바구니에 담았다."

    show roa sad
    h "...어? 하랑이 베개 바꾸게?"

    m "아뇨, 그쪽 겁니다. 바닥에서 자면 뿔이랑 꼬리 아프다면서요."

    h "진짜 나 주는 거야...? 나 이거 평생 안고 잘 거야아아!"

    "로아가 내 허리를 와락 끌어안았다."

    scene bg_street_night with fade
    "노란 베개를 꼭 안고 콧노래를 부르는 악마와 함께 돌아가는 길."

    hide roa with dissolve
    scene bg_room_night with fade

    show roa smile at center with dissolve
    h "으아아... 노란 베개 푹신해... 잘 자, 하랑아!"
    m "...잘 자요."

    hide roa with dissolve
    jump chapter_7_sunday_morning

# =================================----------------===
# [7] 일요일 아침 & 여동생 연하진의 난입 (데모 클리프행어)
# =================================----------------===

label chapter_7_sunday_morning:
    scene bg_room_day with fade

    "일요일 아침. 로아는 사준 노란 베개를 꼭 껴안고 침을 흘리며 자고 있었다."

    play sound sfx_door
    "똑. 똑. 똑."
    "규칙적이고 날카로운 노크 소리가 현관문 너머에서 울렸다."

    m "...택배인가?"

    "아니다. 가문 시절 내 방문을 두드리던 훈육관의 소리와 같았다. 등줄기에 소름이 끼쳤다."

    m "누, 누구세요...?"

    show hajin normal at right with dissolve
    j "문 열어, 오빠."

    play sound sfx_crash
    "쿵-!"

    "연하진. 여우 퇴마사 가문의 천재이자 내 여동생."
    "도어락을 해제하자 단정한 검은 정장 차림의 하진이가 차가운 눈매로 서 있었다."

    play music bgm_wafu fadein 1.0

    j "연락도 없이 집을 나가버리더니... 고작 이런 빈민굴 같은 곳에 숨어 있었어?"

    # =================================----------------===
    # 스팀 넥스트 페스타 데모 종료 지점
    # =================================----------------===
    jump demo_end

# =================================----------------===
# [8] 스팀 넥스트 페스타 데모 종료 화면 및 크레딧
# =================================----------------===

label demo_end:
    scene black with fade
    stop music fadeout 2.0
    stop ambient fadeout 2.0
    
    "스팀 넥스트 페스타 데모 버전을 플레이해 주셔서 감사합니다!"
    "연하랑과 서로아, 그리고 가문과의 본 스토리는 정식 출시 버전에서 계속됩니다."

    menu:
        "스팀 페이지에서 찜하기 (Wishlist)":
            $ open_steam_store_overlay("5036480")
            jump credits

        "메인 메뉴로 돌아가기":
            jump credits

label credits:
    scene black with fade
    stop music fadeout 3.0
    
    "■ Character Illustration"
    "서로아 스탠딩: なかば (https://mode.booth.pm/)"
    "연하진 스탠딩: 子冬さくら (https://kofuyusakura.booth.pm/)"
    
    " "
    "■ Background Illustration"
    "자취방 & 고깃집 배경: みにくる (https://quunplant.booth.pm/)"
    "편의점 배경: 株式会社XERO"

    " "
    "■ Music & BGM"
    "DOVA-SYNDROME (https://dova-s.jp/)"
    "- 切ない海辺 by Yuli"
    "- 和風庭園 by alaki paca"
    "- Noct by shimtone"
    "- 何気ない日常の中の光 by alaki paca"
    
    $ renpy.pause(3.0)
    jump demo_thanks

label demo_thanks:
    "여러분의 관심과 찜하기(Wishlist)는 개발자에게 가장 큰 힘이 됩니다."
    $ renpy.pause(2.0)
    return