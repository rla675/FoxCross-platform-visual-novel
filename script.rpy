# ==============================================================================
# [0] 게임 진행 변수 및 시스템 설정
# ==============================================================================
# 플레이어 선택 및 호감도 시스템
default roa_affection = 0
default dog_purified = False
default bought_special_gift = False
default preferences.sfx_volume = 1.0
define Tab = "Tab" 

# ==============================================================================
# [1] 키맵 설정 및 매너 모드 기능 (Boss Key)
# ==============================================================================
init 999 python:
    # 비주얼 노벨 표준 조작감: Ctrl 키 전담 스킵 설정 (LCTRL / RCTRL 누르고 있는 동안 고속 넘기기)
    config.keymap['skip'] = ['K_LCTRL', 'K_RCTRL']
    config.keymap['toggle_skip'] = []

    # 기존 키맵(스킵 등)에서 Tab 키 완전히 제거 (고속 스킵 오작동 원천 차단)
    for action in list(config.keymap.keys()):
        if action != 'toggle_manner_mode':
            config.keymap[action] = [k for k in config.keymap[action] if k not in ('K_TAB', 'tab', 'shift_K_TAB', 'repeat_K_TAB', 'repeat_tab')]

    # 매너 모드 전용 키로 Tab 등록 (K_TAB 및 tab 모두 등록)
    config.keymap['toggle_manner_mode'] = ['K_TAB', 'tab']

    # 키맵 캐시 갱신 (미호출 시 기존 toggle_skip 유지 버그 방지)
    try:
        renpy.clear_keymap_cache()
    except Exception:
        try:
            renpy.display.behavior.clear_keymap_cache()
        except Exception:
            pass

    # 매너 모드로 일시 정지된 채널 추적 리스트
    manner_paused_channels = []

    # 매너 모드 토글 함수
    def toggle_manner():
        global manner_paused_channels
        if renpy.get_screen("manner_overlay"):
            renpy.hide_screen("manner_overlay")
            channels_to_unpause = manner_paused_channels if manner_paused_channels else ['music', 'ambient']
            for ch in channels_to_unpause:
                try:
                    renpy.music.set_pause(False, channel=ch)
                except Exception:
                    pass
            manner_paused_channels = []
        else:
            try:
                renpy.stop_skipping()
            except Exception:
                pass
            manner_paused_channels = []
            for ch in ['music', 'sound', 'voice', 'ambient']:
                try:
                    is_playing = False
                    try:
                        is_playing = renpy.music.is_playing(channel=ch) or bool(renpy.music.get_playing(channel=ch))
                    except Exception:
                        is_playing = False

                    already_paused = False
                    try:
                        already_paused = bool(renpy.music.get_pause(channel=ch))
                    except Exception:
                        already_paused = False

                    if is_playing and not already_paused:
                        renpy.music.set_pause(True, channel=ch)
                        manner_paused_channels.append(ch)
                except Exception:
                    pass
            renpy.show_screen("manner_overlay")
        renpy.restart_interaction()

    # 키 리스너 상시 표시 등록 (메뉴 및 대화 상자 숨김 상태에서도 동작하도록 보장)
    if hasattr(config, "always_shown_screens"):
        if "manner_key_listener" not in config.always_shown_screens:
            config.always_shown_screens.append("manner_key_listener")
    if "manner_key_listener" not in config.overlay_screens:
        config.overlay_screens.append("manner_key_listener")


# 키 입력 감지 스크린
screen manner_key_listener():
    zorder 99998
    key "toggle_manner_mode" action Function(toggle_manner)
    key "K_TAB" action Function(toggle_manner)
    key "tab" action Function(toggle_manner)

# 매너 모드 덮개 스크린
screen manner_overlay():
    modal True
    zorder 99999
    key "toggle_manner_mode" action Function(toggle_manner)
    key "K_TAB" action Function(toggle_manner)
    key "tab" action Function(toggle_manner)
    key "dismiss" action NullAction()
    button:
        xfill True
        yfill True
        action NullAction()
    add Solid("#000000")
    vbox:
        align (0.5, 0.5)
        spacing 15
        text "MANNER MODE ACTIVE" color "#ffffff" size 36 bold True align (0.5, 0.5)
        textbutton "Press [[Tab] to Resume":
            action Function(toggle_manner)
            text_color "#888888"
            text_size 20
            text_hover_color "#ffffff"
            align (0.5, 0.5)

# ==============================================================================
# [2] 오디오 채널, 변수 및 에셋 정의
# ==============================================================================
init python:
    renpy.music.register_channel("ambient", mixer="sfx", loop=True)

    def find_audio(filename, default_path):
        candidates = [
            default_path,
            "audio/sfx/" + filename,
            "audio/bgm/" + filename,
            "audio/" + filename,
            "sfx/" + filename,
            "bgm/" + filename,
            filename
        ]
        for path in candidates:
            try:
                if renpy.loadable(path):
                    return path
            except Exception:
                pass
        return default_path

# 오디오 에셋
define audio.bgm_main = find_audio("bgm.mp3", "audio/bgm/bgm.mp3")
define audio.bgm_daily = find_audio("bgm1.mp3", "audio/bgm/bgm1.mp3")
define audio.bgm_sad = find_audio("bgm2.mp3", "audio/bgm/bgm2.mp3")
define audio.bgm_wafu = find_audio("bgm3.mp3", "audio/bgm/bgm3.mp3")

define audio.sfx_door = find_audio("sfx_door.mp3", "audio/sfx/sfx_door.mp3")
define audio.sfx_bell = find_audio("sfx_bell.mp3", "audio/sfx/sfx_bell.mp3")
define audio.sfx_hit = find_audio("sfx_hit.mp3", "audio/sfx/sfx_hit.mp3")
define audio.sfx_crash = find_audio("sfx_crash.mp3", "audio/sfx/sfx_crash.mp3")
define audio.sfx_magic = find_audio("sfx_magic.mp3", "audio/sfx/sfx_magic.mp3")

# 캐릭터 정의
define h = Character("서로아", color="#FF5C5C")
define m = Character("연하랑", color="#7CE87C")
define j = Character("연하진", color="#8C9EFF")
define y = Character("유나", color="#FFD180")
define g = Character("가주(연무진)", color="#B0BEC5")

# 배경 이미지 정의
image bg_room_day = "images/bg/home.jpg"
image bg_room_sunset = Transform("images/bg/home.jpg", matrixcolor=TintMatrix("#ffccaa") * BrightnessMatrix(-0.15))
image bg_room_night = Transform("images/bg/home.jpg", matrixcolor=TintMatrix("#4c607a") * BrightnessMatrix(-0.35))
image bg_room_rain = Transform("images/bg/home.jpg", matrixcolor=TintMatrix("#3b4a5a") * BrightnessMatrix(-0.45))
image bg_restaurant_night = "images/bg/meat.jpg"
image bg_store_day = "images/bg/bg23_01.jpg"
image bg_store_night = Transform("images/bg/bg23_01.jpg", matrixcolor=TintMatrix("#4c607a") * BrightnessMatrix(-0.35))
image bg_store_interview = Transform("images/bg/bg24_01.jpg", matrixcolor=TintMatrix("#4c607a") * BrightnessMatrix(-0.30))
image bg_arcade = "images/bg/bg25_01.jpg"
image bg_street_night = Solid("#243342")
image bg_street_rain = Solid("#151d26")
image bg_alley_night = Solid("#0b0f14")
image cg_true_ending = Solid("#fff0e6")

# 캐릭터 스프라이트
image hajin normal = Transform("images/character/10_suit_normal.png", zoom=0.35, yalign=1.0)
image hajin angry = Transform("images/character/10_suit_angry.png", zoom=0.35, yalign=1.0)
image hajin laugh = Transform("images/character/10_suit_laugh.png", zoom=0.35, yalign=1.0)
image hajin damage = Transform("images/character/10_suit_damage.png", zoom=0.35, yalign=1.0)

image roa normal = Transform("images/character/roa_normal.png", zoom=0.35, yalign=1.0)
image roa smile = Transform("images/character/roa_smile.png", zoom=0.35, yalign=1.0)
image roa sad = Transform("images/character/roa_sad.png", zoom=0.35, yalign=1.0)
image roa blush = Transform("images/character/roa_blush.png", zoom=0.35, yalign=1.0)
image roa angry = Transform("images/character/roa_angry.png", zoom=0.35, yalign=1.0)

# ==============================================================================
# [3] 메인 시나리오
# ==============================================================================

label start:
    show screen manner_key_listener
    scene black with fade
    play music bgm_main fadein 1.5

    "세상은 겉보기엔 질서정연하게 굴러가는 듯하지만, 짙은 어둠이 내린 뒷골목 이면에는 인간의 탈을 쓰고 숨죽여 살아가는 영물과 요괴들이 존재한다."
    "물론 현대 사회의 눈부신 가로등 아래에서 뿔이나 꼬리, 혹은 짐승의 귀 같은 이형의 흔적을 드러내며 활보할 수는 없는 노릇이다."
    "미지의 것은 필연적으로 공포를 낳고, 인간의 공포는 언제나 맹목적인 배척과 잔혹한 폭력으로 치닫기 마련이니까."
    "따라서 마계에서 넘어온 악마든, 산야를 지키는 영물이든 자신의 이질적인 기운을 갈무리해 평범한 사람으로 위장하는 환술을 가장 먼저 배운다."
    "그들의 진짜 모습은 마력이 바닥나거나, 치명상을 입어 제어가 풀렸을 때만 아주 찰나의 순간 드러날 뿐이다."
    "…적어도 내가 10년이 넘는 세월 동안 몸담았던, 유서 깊고 가혹한 '여우 퇴마사' 가문에서 뼛속까지 주입받은 상식은 그랬다."

    scene bg_room_night with fade
    play sound sfx_door

    m "으아아...."
    "끼기긱- 쾅."
    "낡아빠진 철제 현관문이 신경을 긁는 쇳소리를 토해내며 닫혔다. 하루 종일 거리를 헤매느라 부르튼 발에서 운동화를 벗어 던진 나는 바닥에 무너지듯 주저앉았다."
    m "하아... 오늘도 영혼까지 탈탈 털렸네."
    "온몸의 뼈마디가 비명을 지르는 듯했다. 퇴마사 가문이라는 거창한 족쇄를 제 발로 끊어내고 나왔을 때만 해도, 내 능력으로 작고 평범한 일상을 지켜내며 살 수 있을 줄 알았다."
    "하지만 현실은 요괴의 가죽보다 냉혹했다. 요괴의 기맥을 읽고 정화하는 법은 익숙했지만, 낯선 사람의 눈을 쳐다보고 이력서를 내미는 법은 단 한 번도 배운 적이 없었다."
    "대인기피증에 짓눌린 나에게, 사람들이 북적이는 거리는 악령의 소굴보다 숨 막히고 차가운 공간이었다."
    "결국 내게 남은 건 텅 빈 통장 잔고 1,400원과, 유통기한이 간당간당한 컵라면 두 개. 그리고 비가 오면 곰팡내가 진동하는 4평짜리 단칸방뿐이다."

    "무거운 한숨을 내쉬며 젖은 겉옷을 벗으려던 찰나였다."
    m "...어?"
    "방 한구석. 내가 이 허름한 방에서 유일하게 아끼는, 길가에서 주워 와 겨우 닦아놓은 낡은 2인용 소파 위에 누군가 웅크려 누워 있었다."

    show roa normal at center with dissolve
    "창문 틈으로 스며든 창백한 달빛 아래, 비현실적인 실루엣이 드러났다."
    "풍성하고 칠흑처럼 짙은 흑발. 그런데 머리칼 끝자락만은 방금 붉은 물감을 칠한 듯 선명한 핏빛을 머금고 있었다."
    "그리고 머리 위로 돋아난 매끄러운 두 개의 뿔. 허리 뒤로는 화살촉 모양의 붉은 꼬리가 축 늘어져 있었다."

    play sound sfx_hit
    with vpunch
    m "아, 악마 꼬리?!"
    "기겁한 채 뒷걸음질 치다 벽에 등을 쿵 부딪혔다."
    m "아니, 인간계에 올라왔으면 최소한 뿔이랑 꼬리 정도는 숨기고 다니는 게 기본 상식 아닙니까?!"

    show roa smile
    h "음냐... 하랑아, 왔어? 오늘 밖에서 맛있는 냄새는 안 묻혀왔니?"
    "녀석은 제 집 안방인 양 눈을 비비며 나른하게 기지개를 켰다. 창백한 피부 위로 보석 같은 투명한 자줏빛 눈동자가 나를 올려다보았다."
    "심지어 내 이름을 정확히 알고 있었다."

    m "누, 뉘신데요?! 내 방엔 어떻게 들어왔고, 내 이름은 또 어떻게 아는 겁니까?!"

    show roa sad
    h "아하하, 그렇게 험악하게 굴지 마... 나 지금 정기가 너무 없어서 환술을 유지할 마력이 1도 없단 말이야."
    "화살촉 모양의 꼬리가 힘없이 장판 바닥을 쓸었다. 젖은 목소리에는 깊은 피로와 애처로움이 배어 있었다."
    h "동네를 떠돌다가 결계가 제일 헐겁고 따뜻한 집을 찾다 보니 여기였어. 이름은... 우편함에 적혀 있던 걸 읽었지."
    h "비까지 맞아서 오들오들 춥단 말이야. 이대로 쫓아내면 나 진짜 길바닥에서 바싹 말라 소멸할지도 몰라..."

    m "저는 쫓겨난 '퇴마사'거든요? 아무리 몰락했어도 악마를 보면 즉시 제압하거나 협회에 넘겨야 마땅한 입장이라고요!"

    show roa normal
    h "흐응... 과연 잔고 1,400원짜리 퇴마사 도련님이 나를 잡을 수 있을까?"
    show roa smile
    h "대신 나를 얹혀살게 해주면... 청소도 열심히 하고, 맛있는 것도 해줄게! 정기 아주 쪼~끔만 나눠주면 안 돼? 응?"

    m "하..."
    "(어이가 없어서 헛웃음이 나온다. 하지만 사람을 해치려는 악독한 마기는 느껴지지 않는다...)"
    "무엇보다 추위에 바들바들 떨리는 저 작은 어깨를 보고 있자니, 가문에서 내쳐져 빗속을 헤매던 내 첫날밤이 겹쳐 보였다. 지독하게 춥고 외로웠던 그날의 기억이."

    m "좋습니다. 단, 세 가지 조건이 있습니다."
    show roa smile
    h "정말?! 역시 우리 하랑이 최고!"
    m "첫째, 허락 없이 강제로 정기를 빼앗지 말 것. 둘째, 집안일은 반반. 셋째, 그 소파는 제 자리니까 당장 내려오세요."

    show roa angry
    h "치... 쩨쩨하긴!"
    show roa sad
    "서로아라고 자신을 소개한 악마는 입술을 삐죽이면서도 얌전히 소파에서 내려왔다."

    "잠시 후, 삐걱거리는 밥상 위에 김이 피어오르는 컵라면 두 개가 놓였다."
    "600원짜리 초라한 편의점 라면. 내 구차한 삶의 단면 같은 음식 앞에서..."
    "로아는 덜덜 떨리는 두 손으로 뜨거운 라면 용기를 소중하게 감싸 쥐었다."

    show roa smile
    h "...따뜻해."
    m "화상 입습니다. 얼른 드시기나 하죠."
    h "하랑아."
    m "왜요. 김치는 없습니다."
    show roa sad
    h "고마워... 가장 춥고 비참할 때, 쫓아내지 않아 줘서."
    h "이 라면... 마계의 차가운 궁전에서 먹었던 그 어떤 산해진미보다 훨씬 따뜻해."

    "장난기 넘치던 얼굴 뒤로 얼핏 스친 짙은 고독. 나는 모르는 척 나무젓가락을 쪼갰다."
    m "...다 불어 터집니다. 쓸데없는 소리 말고 먹기나 해요."

    # 첫날밤 선택지
    "라면을 비우고 나자 당장 잠자리가 문제였다. 바닥에 웅크린 로아는 뿔과 꼬리가 장판에 배겨 불편한지 몸을 뒤척였다."
    menu:
        "내가 아끼는 두꺼운 솜이불을 로아에게 양보한다.":
            $ roa_affection += 2
            m "이불 두껍게 깔고 자요. 새벽엔 바닥에서 한기 올라오니까."
            show roa smile
            h "어...? 하랑이는 얇은 담요 하나뿐이잖아... 진짜 고마워! 헤헤, 하랑이 의외로 엄청 다정하네!"
        "소파 쿠션을 바닥에 깔아주고 규칙을 엄격히 강조한다.":
            $ roa_affection += 1
            m "쿠션이라도 대고 자요. 소파를 내줄 순 없지만 병나면 곤란하니까요."
            show roa normal
            h "우응... 조금 딱딱하지만 그래도 길바닥보단 백배 낫다! 잘 자, 하랑아."

    jump ch02_job_search

label ch02_job_search:
    scene bg_room_day with fade
    play music bgm_daily fadein 1.0

    "창문 틈으로 들어오는 아침 햇살과 함께 눈을 떴다."
    m "으음..."
    "가슴팍이 묵직해 내려다보니, 로아가 둘둘 만 이불을 끌어안고 내 발치에 붙어 곤히 잠들어 있었다."
    "심지어 푹신한 붉은 꼬리가 스멀스멀 올라와 내 턱 밑을 간지럽히고 있었다."

    m "꿈이... 아니었군."
    "머리 위에 삐죽 솟은 뿔을 살짝 톡 치자, 로아가 번쩍 눈을 떴다."
    show roa blush at center with dissolve
    h "으응... 뿔 건드리지 마... 거기 엄청 예민하단 말이야..."
    show roa smile
    h "하랑아, 좋은 아침! 인간계 이불은 진짜 천국이야!"

    m "잔고 1,400원입니다. 오늘 당장 알바를 구하지 않으면 오늘 저녁은 굶어야 해요."
    show roa angry
    h "단식은 절대 반대야! 고기... 고기 맛 나는 거라도 먹어야 해!"
    show roa smile
    h "나도 따라갈래! 뿔이랑 꼬리 마력으로 꽁꽁 숨기고 얌전히 뒤에만 있을게. 너 혼자 가면 사람 눈치 보느라 편의점 문도 못 열 것 같단 말이야!"
    m "우, 울컥하게 진짜..."

    hide roa with dissolve
    scene bg_store_interview with fade

    "골목 모퉁이에 자리한 '달빛 편의점'. 유리창에 '야간 알바 급구' 종이가 붙어 있었다."
    m "(침착하자. 숨 들이마시고... 이력서만 드리고 오는 거야.)"
    "문 손잡이를 쥔 손이 잘게 떨렸다. 낯선 사람에게 나를 내보여야 한다는 두려움에 발이 굳어버렸을 때—"

    show roa smile at right with dissolve
    h "하랑아, 파이팅! 문밖에서 내가 응원 댄스 추고 있을게!"
    "유리창 너머로 로아가 양 주먹을 쥐고 엉덩이를 씰룩이며 괴상한 춤을 추고 있었다."
    m "...푸흡."
    "어이없는 춤사위에 긴장이 탁 풀렸다. 심장이 안정을 찾았다."

    hide roa with dissolve
    play sound sfx_bell
    "딸랑-"
    "나는 카운터의 지친 점장님께 공손히 이력서를 건넸다."

    scene black with fade
    pause 1.0

    scene bg_room_day with fade
    "그리고 이틀 뒤."
    "합격 연락이 오지 않아 초조하게 휴대전화만 만지작거리던 그때—"
    play sound sfx_hit
    "지잉-! 지잉-!"
    "[[달빛편의점: 점장입니다. 성실해 보이셔서 마음에 듭니다. 오늘 밤 10시부터 야간 근무 가능하신가요?]]"

    m "합... 합격이다!"
    show roa smile at center with dissolve
    h "와아아아! 우리 하랑이 대단해! 최고야!!"
    "로아는 껑충껑충 뛰며 내 두 손을 잡고 방 안을 빙글빙글 돌았다."
    "타인과의 접촉을 그토록 무서워하던 내가, 이 순간만큼은 이 온기를 떨쳐내고 싶지 않았다."

    hide roa with dissolve
    jump ch03_night_shift

label ch03_night_shift:
    scene bg_store_night with fade
    play music bgm_main fadein 1.0

    "새벽 3시 20분."
    "적막한 편의점 안에는 냉장고 모터 소리와 잔잔한 새벽 라디오만 흘렀다."
    "손님이 드문 새벽 시간은 대인기피증이 있는 내게 오히려 평화로운 도피처 같았다."

    play sound sfx_bell
    "딸랑-!"
    "후드티를 푹 눌러쓴 작은 체구가 들어왔다. 바지 엉덩이 부분이 불룩하게 솟아 흔들리는 꼴이 영락없이 꼬리를 감춘 모양새였다."

    show roa normal at center with dissolve
    m "하... 로아 씨. 야밤에 여긴 왜 왔어요?"
    show roa smile
    h "헤헤, 짠! 야식 챙겨왔지!"
    "보온병에 담아온 뜨거운 물과 컵라면. 카운터에 나란히 앉아 면을 후루룩 넘겼다."

    m "고마워요. 심심했는데 시간은 잘 갔네요."
    h "……."
    "대답이 없어 돌아보니, 로아의 눈동자가 핏빛으로 붉게 물들어 있었다. 거칠어진 숨결."

    show roa blush
    play sound sfx_magic
    "달콤하면서도 아찔한 마기가 좁은 카운터를 가득 채웠다. 로아가 내 가슴팍으로 덮쳐왔다."
    h "하랑아... 네 정기가... 너무 달콤해... 조금만... 한 입만..."
    "튀어나온 붉은 꼬리가 내 허벅지를 뱀처럼 감쌌다."
    "원초적인 공포가 스쳤지만, 녀석의 어깨가 필사적으로 본능을 참아내느라 덜덜 떨리고 있는 것이 보였다."

    play sound sfx_hit
    with hpunch
    "딱-!"
    m "집주인과의 규칙 1번, 어기면 쫓아냅니다."
    show roa angry
    h "아얏?!"
    "이마를 맞은 로아의 눈이 원래의 자줏빛으로 돌아왔다. 제 자세를 깨달은 녀석의 얼굴이 터질 듯 달아올랐다."

    show roa sad
    h "하, 하랑아! 미안해... 나 진짜 나쁜 악마 아니야, 쫓아내지 마..."
    m "...안 쫓아냅니다. 아침에 퇴근하면 제대로 된 밥 해줄 테니 버텨봐요."
    show roa smile
    h "응! 절대 안 질게!"

    hide roa with dissolve
    jump ch04_energy_share

label ch04_energy_share:
    scene bg_room_day with fade
    play music bgm_daily fadein 1.0

    "집으로 돌아와 첫 야간 알바 일당 봉투를 손에 쥐었다. 뿌듯함과 함께 깊은 피로가 몰려왔다."
    show roa sad at center with dissolve
    "구석에서 눈치를 보며 웅크린 로아의 뿔이 파르르 떨리고 있었다. 한계였다."

    m "로아 씨, 이리 와요."
    show roa blush
    h "응...? 나 또 본능 터질까 봐 무서운데..."
    m "주말이니까 저 좀 쓰러져 자도 괜찮습니다. 손 줘요."

    "차갑게 식은 로아의 작은 손을 잡고 내 품으로 끌어당겼다."
    "단전에 잠들어 있던 맑은 황금빛 양기를 끌어올려 그녀에게 흘려보냈다."
    play sound sfx_magic
    h "아... 앗... 너무 따뜻해... 몸이 녹아내릴 것 같아..."
    "로아는 내 어깨에 이마를 파묻고 내 옷자락을 꽉 쥐었다."

    m "...오늘은 여기까지."
    show roa smile
    "화색이 돌며 생기를 되찾은 로아가 감격에 차서 내 목을 끌어안았다."
    h "와아! 기운이 펄펄 넘쳐! 평생 하랑이한테 충성할게!"
    m "얼른 떨어져요! 배고프니까 씻고 올 동안 찌개나 끓여요!"

    hide roa with dissolve
    jump ch05_cooking

label ch05_cooking:
    scene bg_room_sunset with fade
    play music bgm_daily fadein 1.0

    "잠에서 깨어나니 보글보글 찌개 끓는 구수한 냄새가 코를 찔렀다."
    show roa normal at center with dissolve
    "앞치마를 두르고 국자를 든 로아가 까치발을 하고 서 있었다."

    show roa smile
    h "하랑아, 깼어? 일당 봉투에서 딱 만 원만 빼서 마트 다녀왔지!"
    "식탁 위에는 갓 끓인 돼지고기 김치찌개와 하얀 쌀밥이 정갈하게 차려져 있었다."
    m "직접... 칼질해서 끓인 겁니까?"
    h "유튜브 보고 피나게 연습했어! 얼른 먹어봐!"

    "한 숟가락 입에 넣었다. 조금 짜고 고기는 살짝 질겼지만..."
    m "...인생에서 먹어본 찌개 중에 제일 맛있네요."
    show roa smile
    h "진짜?! 와아! 밥 더 줄게, 많이 먹어!"
    "얼어붙어 있던 마음이 따뜻한 국물에 사르르 풀려나갔다."

    hide roa with dissolve
    jump ch06_shopping

label ch06_shopping:
    scene bg_store_day with fade
    "식사를 마치고 필요한 생필품을 사러 대형 마트로 향했다."
    show roa smile at center with dissolve
    h "우와! 하랑아, 여기 번쩍거리는 거 엄청 많아!"
    "로아는 빨간 칫솔과 연두색 칫솔을 들고 흔들었다."
    h "이거 봐! 우리 커플 칫솔 하자!"
    m "커, 커플은 무슨... 아무거나 사요!"

    "수면 코너를 지나다 노란색 푹신한 베개가 눈에 들어왔다."
    menu:
        "로아를 위해 노란색 푹신한 베개를 장바구니에 담는다.":
            $ roa_affection += 2
            $ bought_special_gift = True
            m "이거 가져가요. 맨날 뿔 배긴다고 징징댔잖아요."
            show roa sad
            h "진짜...? 인간계 와서 내 전용 물건 처음 생겨봐... 나 이거 평생 안 버릴래!"
            show roa blush
            "로아는 마트 한복판에서 베개를 껴안고 내 허리를 와락 끌어안았다."
        "가장 저렴한 기본 베개를 고른다.":
            $ roa_affection += 1
            m "이거 쓰세요. 가성비가 제일 낫네요."
            show roa smile
            h "헤헤, 하랑이가 골라준 거면 뭐든 좋아!"

    hide roa with dissolve
    jump ch07_regular_customer

label ch07_regular_customer:
    scene bg_store_night with fade
    play music bgm_daily fadein 1.0

    "며칠 뒤 새벽, 편의점에 반가운 손님이 찾아왔다. 인근 대학생 유나였다."
    show roa normal at left with dissolve
    "카운터 아래에 웅크려 과자를 먹던 로아가 귀를 쫑긋 세웠다."

    y "저기, 알바생 오빠! 저번에 추천해주신 캔커피 진짜 맛있더라고요. 과제 밤샘하는데 덕분에 살았어요!"
    m "아... 다, 다행이네요. 밤샘 무리하지 마세요."
    y "오빠는 볼 때마다 참 친절하고 차분하신 것 같아요. 이거 마시면서 일하세요!"
    "유나가 캔커피 하나를 건네며 상냥하게 웃고 나갔다."

    show roa angry at center with dissolve
    h "흥! 칫! 핏!"
    m "뭐가 또 불만입니까?"
    h "오빠아~? 친절하고 차분해애~? 나한테는 만날 눈 흘기면서 저 여대생한텐 완전 천사표네!"
    m "손님한테 친절한 건 알바의 기본이죠. 질투합니까?"
    show roa blush
    h "누, 누가 질투를 해! 난 그냥 커피 캔에 뿔 들이받고 싶을 뿐이야!"
    "볼을 부풀리는 로아의 모습에 나도 모르게 웃음이 터져 나왔다. 사람과 대화하는 것이 더 이상 무섭지 않았다."

    hide roa with dissolve
    jump ch08_meat_feast

label ch08_meat_feast:
    scene bg_restaurant_night with fade
    play music bgm_daily fadein 1.0

    "첫 월급날 저녁. 나는 큰맘 먹고 로아를 동네 고깃집으로 데려왔다."
    show roa smile at center with dissolve
    h "하랑아... 진짜 삼겹살 구워 먹는 거야?! 냄새만 맡아도 기절할 것 같아!"
    m "한 달 동안 고생 많았으니까요. 오늘만큼은 배 터지게 먹어요."

    "지글지글 고기가 익어가고, 로아는 볼이 터져라 쌈을 싸서 입에 넣었다."
    h "우물우물... 하랑아, 아~ 해봐! 너도 먹어야지!"
    "로아가 내민 상추쌈. 어색하게 받아먹자 녀석이 배시시 웃었다."

    show roa sad
    h "나... 마계에선 늘 쓸모없는 열등생이라고 구박만 받았어. 누구도 나한테 고기를 구워주거나 따뜻하게 대해준 적 없었거든."
    h "하랑이를 만난 건... 내 생애 가장 큰 행운이야."
    m "...저도 마찬가지입니다. 가문에서 쫓겨나 혼자 썩어가던 절 사람으로 만들어준 건 로아 씨니까요."
    "시끌벅적한 고깃집 연기 너머로, 서로를 바라보는 눈빛이 깊어져 갔다."

    hide roa with dissolve
    jump ch09_arcade

label ch09_arcade:
    scene bg_arcade with fade
    "배를 두드리며 번화가를 걷다 오락실 인형 뽑기 기계 앞에 멈춰 섰다."
    show roa smile at center with dissolve
    h "헉! 저 하얀 여우 인형... 하랑이 닮았어! 갖고 싶다!"
    m "저런 건 상술입니다. 돈 낭비예요."
    show roa sad
    h "우응... 그렇겠지..."

    "시무룩한 꼬리를 보자 지갑을 열지 않을 수 없었다."
    m "딱 오천 원만 씁니다."
    "퇴마사의 기맥 집중 기술을 인형 뽑기 집게에 미세하게 실었다."
    play sound sfx_hit
    with hpunch
    "덜컹, 툭!"

    show roa smile
    h "와아아아! 뽑았다! 하랑이 진짜 최고!!"
    "여우 인형을 품에 안고 내 손을 덥석 잡는 로아. 잡힌 손을 빼지 않고 나란히 밤길을 걸었다."

    hide roa with dissolve
    jump ch10_alley_spirit

label ch10_alley_spirit:
    scene bg_alley_night with fade
    "며칠 뒤 새벽 4시. 편의점 뒷골목에서 음산한 마기가 감돌았다."
    m "...누구냐."
    "어둠 속에서 발톱을 드러낸 것은, 굶주림에 미쳐버린 하급 요괴였다."
    play sound sfx_magic
    "부적으로 쳐내자 드러난 본모습은 비쩍 마른 강아지의 유령이었다."

    show roa sad at center with dissolve
    h "하랑아, 잠깐만... 쟤, 울고 있어. 버림받은 골목에서 주인을 기다리다 원령이 된 거래..."
    "강아지 요괴가 내 신발 코에 머리를 비비며 낑낑거렸다."

    menu:
        "정기를 나누어주고 따뜻하게 정화해 준다.":
            $ roa_affection += 3
            $ dog_purified = True
            m "따뜻한 게 필요했다면 진작 말하지 그랬어."
            "단전의 맑은 황금빛 기운으로 강아지를 감쌌다. 흉측한 외형이 눈부신 빛가루로 변하며 평온하게 성불했다."
            show roa blush
            h "하랑아... 넌 세상에서 제일 다정한 사람이야."
        "퇴마사의 율법대로 단호하게 소멸시킨다.":
            $ roa_affection -= 1
            m "규칙은 지켜야 합니다."
            "차가운 부적으로 소멸시켰다. 로아의 얼굴에 그늘이 드리웠다."

    hide roa with dissolve
    jump ch11_first_fight

label ch11_first_fight:
    scene bg_room_day with fade
    play music bgm_wafu fadein 1.0

    play sound sfx_door
    "똑. 똑. 똑."
    "소름 끼치도록 반듯한 노크 소리."
    show hajin normal at right with dissolve
    j "문 열어, 오빠."

    "가문의 천재이자 여동생인 연하진이었다."
    j "가문에서 잠적하더니 고작 이런 빈민굴에... 냄새가 역겹네. 악마를 키우고 있었어?!"


    show roa sad at left with dissolve
    "잠에서 깬 로아를 발견한 하진이의 손에서 서늘한 푸른 부적이 튀어나왔다."
    j "당장 목을 치겠어."

    play sound sfx_magic
    with vpunch
    "부적이 쇄도하는 순간, 나는 몸을 날려 로아의 앞을 가로막았다."
    m "손대지 마. 이 녀석은 내 식구다."

    show hajin angry
    j "가문의 수치 주제에 감히 누굴 지키겠다고?!"
    "수십 장의 얼음 칼날이 날아들었다. 나는 단전의 황금빛 양기를 전면으로 펼쳐냈다."
    m "파(破)!"
    "챙, 채쟁-! 살기 없는 순수한 정화의 장막에 하진의 칼날이 닿자마자 봄눈 녹듯 소멸했다."

    show hajin damage
    j "이게... 무슨 기운이야...?! 살기가 전혀 없는데 내 공격이...!"
    "순식간에 파고들어 하진의 목덜미에 부적을 겨누었다."
    m "퇴마는 학살이 아니라 지키는 거다. 돌아가서 아버지께 전해. 다신 내 앞에 나타나지 말라고."

    show hajin angry
    j "...두고 봐. 가문이 오빠를 영원히 가만두지 않을 테니까!"
    hide hajin with dissolve
    play sound sfx_door

    show roa sad at center with dissolve
    h "으아앙! 나 때문에 다쳤잖아... 나 나갈게..."
    m "바보 같긴. 여긴 로아 씨 집이에요. 내가 지킬 겁니다."

    hide roa with dissolve
    jump ch12_crisis_warning

label ch12_crisis_warning:
    scene bg_store_night with fade
    play music bgm_wafu fadein 1.0

    "폭풍우가 치던 다음 날 새벽, 하진이가 다시 편의점으로 들이닥쳤다."
    show hajin normal at right with dissolve
    j "오빠, 당장 도망쳐. 아버지가 은장급 정예 부대를 이끌고 오늘 밤 여길 쓸어버리기로 했어."
    j "악마를 버리고 숨어. 이건 핏줄로서 주는 마지막 경고야."
    hide hajin with dissolve

    show roa sad at left with dissolve
    "박스 뒤에서 대화를 들은 로아의 얼굴이 하얗게 질려 있었다."
    m "걱정 마요. 내가 지킨다고 했잖아요."
    h "……응."
    "하지만 로아의 눈빛에는 깊은 결심이 서려 있었다."

    hide roa with dissolve
    jump ch13_runaway_rain

label ch13_runaway_rain:
    scene bg_room_rain with fade
    "오후에 눈을 떴을 때, 로아의 온기는 사라져 있었다."
    "노란 베개 위, 여우 인형 옆에 놓인 쪽지."
    "[[하랑아 미안해. 나 때문에 네 평범한 일상이 깨지면 안 돼. 마계로 돌아갈게. 밥 잘 챙겨 먹고 잘 지내.]]"

    m "이 멍청이가 진짜...!!"

    scene bg_street_rain with fade
    play music bgm_sad fadein 1.0
    "장대비 속을 미친 듯이 달렸다. 숨이 턱까지 차오르고 심장이 찢어질 것 같았다."
    "저 멀리 가로등 아래, 비에 젖은 꼬리를 늘어뜨린 채 터덜터덜 걷는 뒷모습."

    m "서로아-!!"
    show roa sad at center with dissolve
    with vpunch
    "얼음장같이 차가운 그녀를 거칠게 와락 끌어안았다."

    h "하랑아, 놓아줘... 나 때문에 다친단 말이야...!"
    m "내 인생에 너 빼면 아무것도 안 남아! 죽어도 내 옆에서 죽고 살아도 내 옆에서 살아! 단 한 발짝도 가지 마!"
    h "흑... 바보... 나도 하랑이 없으면 안 된단 말이야..."
    "빗속에서 서로의 온도를 확인하며 집으로 돌아왔다."

    hide roa with dissolve
    jump ch14_final_battle

label ch14_final_battle:
    scene bg_room_night with fade
    play sound sfx_crash
    with vpunch
    play music bgm_wafu fadein 1.0

    "쾅-!!"
    "현관문이 박살 나며 가주 연무진과 십여 명의 퇴마사들이 들이닥쳤다."
    show hajin angry at right with dissolve
    show roa sad at left with dissolve

    g "더러운 악마와 정을 통한 패륜아 놈. 무릎을 꿇어라."
    m "사사로운 살기만 좇는 가문의 방식엔 절대 굴복하지 않습니다. 내 식구는 내가 지킵니다."
    g "베어라!"

    "사방에서 푸른 부적이 쇄도하는 절체절명의 순간."
    show roa angry
    h "하랑아, 내 마력을 써!"
    "로아가 내 허리를 감싸 안으며 순수한 마력을 쏟아부었다."
    "나의 황금빛 양기와 로아의 자줏빛 마력이 하나로 융합되어 눈부신 소용돌이를 일으켰다."

    m "정(淨)-----!!"
    play sound sfx_magic
    with hpunch
    "파아아아아앙-!!"

    show hajin damage
    "압도적인 황금빛 정화 파동이 방 안을 쓸어버렸다. 퇴마사들의 무기는 빛가루로 부서지고 마력은 온화하게 무력화되었다."
    g "크윽...! 살기가 없는데도 우리를 제압하다니... 오늘부로 넌 가문에서 영구 제명이다!"
    "가주는 굴욕감에 짓눌려 퇴각했고, 하진은 옅은 미소를 남긴 채 어둠 속으로 사라졌다."

    hide hajin with dissolve
    hide roa with dissolve
    jump ch15_farewell

label ch15_farewell:
    scene bg_room_day with fade
    play music bgm_sad fadein 1.0

    "전투가 끝나고 소파에 쓰러지듯 앉았다."
    show roa sad at center with dissolve
    "내 앞에 무릎 꿇은 로아의 몸이 반투명하게 흐려지고 있었다."

    h "하랑아... 아까 마력을 너무 쥐어짜서 내 존재의 근원이 바닥났어."
    h "이대로 있으면 소멸해... 마계의 '심연의 샘'에 들어가서 아주 긴 잠을 자야 할 것 같아. 언제 돌아올 수 있을지 나도 몰라..."
    h "그러니까... 나 갈게."

    m "……."
    "내 세계를 밝혀준 유일한 빛을, 이대로 보내야 하는 걸까."

    menu:
        "로아를 품에 안고 내 모든 정기를 쏟아붓는다.":
            if roa_affection >= 5:
                jump ending_true
            else:
                jump ending_bad
        "로아의 회복을 위해 눈물로 배웅한다.":
            jump ending_normal

# ==============================================================================
# [4] 엔딩 분기
# ==============================================================================

label ending_true:
    m "가지 마."
    show roa blush
    "돌아서려는 로아의 허리를 감아 품에 단단히 가두었다."
    h "하랑아...? 안 돼, 이러면 너까지 위험해..."
    m "소멸하게 둘 바엔 내 목숨을 다 쪼개줄게. 마계의 샘 따위 필요 없어."

    "로아의 이마에 내 이마를 맞대고 단전의 모든 황금빛 생명력을 거침없이 흘려보냈다."
    play sound sfx_magic
    m "내가 매일 밥 해주고, 매일 내 정기로 채워줄게. 내 곁에서 평생 떨어지지 마."

    show roa smile
    h "응... 안 갈게! 마계 따위 다 버릴래! 평생 하랑이 껌딱지 할 거야!"
    "부서진 창문으로 쏟아지는 아침 햇살이 두 사람을 축복하듯 감싸 안았다."

    play music bgm_daily fadein 2.0
    scene cg_true_ending with fade
    pause 1.0

    "그렇게, 통장 잔고 1,400원이던 몰락 퇴마사의 인생에 찾아온 붉은빛 악마와의 기적 같은 진짜 동거는 영원히 이어지고 있었다."
    jump credits

label ending_normal:
    m "...다녀와요."
    "눈물을 삼키며 로아의 머리를 쓰다듬었다."
    m "몸 다 나으면 꼭 우리 집으로 돌아와요. 노란 베개랑 여우 인형, 먼지 안 쌓이게 닦아놓고 기다릴 테니까."

    show roa smile
    h "응! 꼭 올게. 늦더라도 반드시 뛰어올게! 얌전히 기다려야 해, 내 츤데레 짠돌이!"

    play sound sfx_magic
    "로아의 몸이 붉은빛으로 흩어지며 허공으로 사라졌다."
    hide roa with dissolve

    scene bg_room_sunset with fade
    pause 1.0

    "그로부터 1년 뒤."
    "나는 편의점 일을 하며 밤거리의 방황하는 영혼들을 정화하는 삶을 살고 있다."
    m "다녀왔어."
    "방구석에 놓인 여우 인형의 꼬리가 바람도 없는데 살랑 흔들렸다."
    "그리고 코끝을 스치는 달콤하고 그리운 향기. 기나긴 기다림이 끝나가고 있었다."
    jump credits

label ending_bad:
    m "가지 마... 제발 내 곁에 있어줘..."
    show roa sad
    h "하랑아... 미안해. 우리에겐 마력이 너무 부족해..."
    "억지로 기운을 쏟아부었지만, 메마른 기맥은 그녀의 흩어지는 몸을 붙잡지 못했다."
    h "따뜻한 기억 선물해줘서 고마웠어... 안녕..."
    "로아는 한 줌의 재처럼 허공으로 흩어져 사라졌다."
    scene black with fade
    "다시 차갑고 어두운 침묵만이 남은 4평짜리 방. 나는 소파에 웅크린 채 영원히 찾아오지 않을 온기를 기다린다."
    jump credits

# ==============================================================================
# [5] 크레딧
# ==============================================================================
label credits:
    scene black with fade
    stop music fadeout 3.0
    
    " "
    "■ Character Illustration"
    "서로아 스탠딩: なかば (https://mode.booth.pm/)"
    "연하진 스탠딩: 子冬さくら (https://kofuyusakura.booth.pm/)"

    " "
    "■ Background Illustration"
    "자취방 & 고깃집 배경: みにくる (https://quunplant.booth.pm/)"
    "편의점 배경: 株式会社XERO"

    " "
    "■ Music & Sound"
    "DOVA-SYNDROME (https://dova-s.jp/)"
    "- 切ない海辺 by Yuli"
    "- 和風庭園 by alaki paca"
    "- Noct by shimtone"
    "- 何気ない日常の中의 光 by alaki paca"

    pause 3.0
    return
