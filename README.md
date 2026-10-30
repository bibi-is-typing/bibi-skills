# bibi-skills

한국어 글을 다듬고, 프로젝트의 문제부터 결정까지 정리하는 스킬 모음입니다. 한 저장소에서 **Codex**와 **Claude Code**용 스킬을 골라 설치할 수 있습니다.

| 스킬 | 하는 일 | 예시 |
|---|---|---|
| `korean-writing` | 9개 장르의 한국어 리라이팅. 사실·조건·불확실성과 원작자의 말투를 보존합니다. | “이 메일을 짧고 자연스럽게 다듬어줘.” |
| `pm-frame` | 문제 정의 → 근거 → 우선순위 → 대안 → 성공 지표 → 결정문으로 이어지는 6단계 PM 프레임입니다. | “이 기획을 해야 할지 문제 정의부터 질문해줘.” |

## 빠른 설치

Python 3.9 이상과 Git이 필요합니다. 설치 스크립트는 Python 기본 라이브러리만 사용합니다.

```bash
git clone https://github.com/bibi-is-typing/bibi-skills.git
cd bibi-skills
```

사용할 도구에 맞는 명령을 실행합니다.

```bash
# Codex에 두 스킬 설치
python3 scripts/install.py --target codex

# Claude Code에 두 스킬 설치
python3 scripts/install.py --target claude-code

# 두 도구에 모두 설치
python3 scripts/install.py --target both
```

Windows에서 `python3` 명령이 없으면 `python`을 사용합니다. Git 대신 [저장소 ZIP](https://github.com/bibi-is-typing/bibi-skills/archive/refs/heads/main.zip)을 내려받아 압축을 풀고, 그 폴더에서 설치 명령을 실행해도 됩니다.

| 도구 | 배포 폴더 | 기본 설치 위치 | 직접 호출 |
|---|---|---|---|
| Codex | [`codex/`](codex/README.md) | `~/.agents/skills/` | `$korean-writing`, `$pm-frame` |
| Claude Code | [`claude-code/`](claude-code/README.md) | `~/.claude/skills/` | `/korean-writing`, `/pm-frame` |

도구별 위치와 호출 방식은 [OpenAI 공식 안내](https://learn.chatgpt.com/docs/build-skills)와 [Claude Code 공식 안내](https://code.claude.com/docs/en/skills)를 기준으로 합니다. 두 스킬 모두 요청 내용에 맞는 자동 선택을 허용합니다.

## 하나만 설치하거나 기존 설치본 업데이트하기

```bash
# korean-writing만 설치
python3 scripts/install.py --target codex --skill korean-writing

# 파일 변경 없이 설치 계획 확인
python3 scripts/install.py --target both --dry-run

# Git으로 받은 저장소 업데이트 후 설치본 교체
git pull --ff-only
python3 scripts/install.py --target codex --replace
```

기존 스킬이 있으면 기본 설치는 멈춥니다. `--replace`를 붙이면 기존 폴더를 설치 위치의 `.bibi-skills-backups/`에 ZIP으로 백업한 뒤 교체합니다. 백업은 자동으로 삭제하지 않습니다. 두 도구를 업데이트하려면 `--target both --replace`를 사용합니다.

이미 `~/.codex/skills/` 또는 별도의 `CODEX_HOME/skills/`에 설치했다면, 같은 이름이 중복으로 등록되지 않도록 **기존 위치**를 지정합니다.

```bash
python3 scripts/install.py --target codex --dest "$HOME/.codex/skills" --replace
```

설치 스크립트는 기본 Codex 경로와 별도로 기존 `CODEX_HOME/skills/` 설치를 발견하면 위치를 안내하고 멈춥니다. 프로젝트별 설치 방법은 도구별 README를 참고하세요.

## 사용 예시

Codex:

```text
$korean-writing 아래 공지를 자연스럽게 다듬어줘. 일정과 조건은 그대로 유지해줘.

$pm-frame 새 기능 제안을 검토하고 싶어. 문제 정의부터 한 번에 하나씩 질문해줘.
```

Claude Code:

```text
/korean-writing 아래 공지를 자연스럽게 다듬어줘. 일정과 조건은 그대로 유지해줘.

/pm-frame 이 기획서를 점검하고, 근거가 약한 부분부터 짚어줘.
```

`pm-frame`은 인터뷰·기획서 점검·결정문 작성 모드를 지원합니다. 이미 정한 구현이나 버그 수정을 자동으로 PM 인터뷰로 바꾸지 않습니다. 개인 볼트나 다른 스킬이 없어도 사용할 수 있고, 제공받지 못한 자료는 미확인으로 남깁니다.

## 두 버전의 관계

두 도구에서 같은 글쓰기·PM 기준을 사용합니다. Codex판에는 `agents/openai.yaml` 표시 정보와 `$스킬명` 호출 예시가 있고, Claude Code판에는 `/스킬명` 호출과 해당 작업 환경의 저장 안내가 있습니다.

각 스킬 폴더에 필요한 참고 문서가 모두 들어 있습니다. 다른 도구 폴더나 이 저장소의 상위 폴더를 함께 설치할 필요가 없습니다.

```text
bibi-skills/
├── README.md
├── codex/
│   ├── README.md
│   ├── korean-writing/  # SKILL.md, references, examples, agents
│   └── pm-frame/        # SKILL.md, references, agents
├── claude-code/
│   ├── README.md
│   ├── korean-writing/  # SKILL.md, references, examples
│   └── pm-frame/        # SKILL.md, references
├── scripts/            # 설치, 동기화, 검증
└── tests/              # 설치·업데이트 동작 검사
```

## 스킬 수정과 검증

`codex/`를 편집 원본으로 사용합니다. 공통 규칙과 참고 문서를 수정한 뒤 다음 명령으로 Claude Code판을 다시 만듭니다. Claude 전용 변환은 `scripts/sync_claude.py`에서 관리합니다.

```bash
python3 scripts/sync_claude.py
python3 scripts/validate.py
python3 -m unittest discover -s tests -v
```

GitHub Actions에서도 동기화 상태, 필수 파일, 내부 참조와 설치·백업 동작을 검사합니다. 이 검사는 파일 구조와 설치 기능을 확인합니다. 모델의 실제 응답 품질은 사용 사례별로 별도 확인해야 합니다.

## 원본과 변경 사항

| 원본 저장소 | 기준 커밋 |
|---|---|
| [korean-writing](https://github.com/bibi-is-typing/korean-writing) | [`aceb716`](https://github.com/bibi-is-typing/korean-writing/tree/aceb716dcb4e00637d9b2d47fbf7af2dccb478e4) |
| [pm-frame](https://github.com/bibi-is-typing/pm-frame) | [`64f9a2c`](https://github.com/bibi-is-typing/pm-frame/tree/64f9a2cef443078667711a12668af6b2b585788c) |

원본의 9개 글쓰기 장르와 6단계 PM 프레임을 유지했습니다. 원문에 없는 수치 추가, 추측의 단정, 불필요한 질문 강제, 없는 참고 파일·개인 경로 의존성을 보완했습니다. 이 보완은 두 도구용 버전에 함께 반영돼 있습니다.

라이선스 범위는 [LICENSES.md](LICENSES.md)를 참고하세요.
