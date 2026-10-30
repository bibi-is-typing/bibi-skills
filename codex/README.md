# Codex용 스킬

| 스킬 | 설명 |
|---|---|
| [korean-writing](korean-writing/SKILL.md) | 사실과 말투를 보존하는 한국어 리라이팅 |
| [pm-frame](pm-frame/SKILL.md) | 문제 정의부터 결정문까지 이어지는 6단계 PM 프레임 |

각 폴더에 `SKILL.md`, 참고 문서, Codex용 `agents/openai.yaml`이 들어 있습니다.

## 개인 설치

저장소 루트에서 실행합니다.

```bash
python3 scripts/install.py --target codex
```

기본 설치 위치는 `~/.agents/skills/`입니다. 하나만 설치하려면 `--skill korean-writing` 또는 `--skill pm-frame`을 붙입니다.

Codex의 스킬 설치 도우미를 사용할 수도 있습니다.

```text
$skill-installer bibi-is-typing/bibi-skills 저장소의 codex/korean-writing과 codex/pm-frame을 설치해줘. 같은 이름이 이미 있으면 기존 설치 위치를 확인해줘.
```

이미 `~/.codex/skills/`에 설치했다면 기존 위치를 지정해 업데이트합니다.

```bash
python3 scripts/install.py --target codex --dest "$HOME/.codex/skills" --replace
```

`CODEX_HOME`을 별도로 사용 중이면 해당 경로의 `skills` 폴더를 `--dest`에 지정합니다. 같은 스킬을 여러 검색 위치에 설치하면 중복 표시될 수 있습니다.

## 프로젝트에만 설치

```bash
python3 scripts/install.py --target codex --dest /path/to/project/.agents/skills
```

`/path/to/project`를 실제 대상 프로젝트 경로로 바꿉니다. 스크립트가 필요 없으면 `korean-writing/` 또는 `pm-frame/` 폴더 전체를 원하는 skills 폴더로 복사해도 됩니다. `SKILL.md`만 복사하면 참고 문서를 읽을 수 없습니다.

## 호출

```text
$korean-writing 이 이메일의 요청과 기한을 유지하면서 자연스럽게 다듬어줘.

$pm-frame 이 기획서를 6단계 기준으로 점검해줘.
```

요청 내용에 따른 자동 선택도 사용할 수 있습니다. 새 스킬이 표시되지 않으면 새 메시지에서 다시 확인하고, 계속 나타나지 않으면 Codex를 재시작하세요. 검색 위치와 호출 방식은 [OpenAI 공식 스킬 문서](https://learn.chatgpt.com/docs/build-skills)를 참고하세요.

## 업데이트

```bash
git pull --ff-only
python3 scripts/install.py --target codex --replace
```

사용자 지정 위치에 설치했다면 같은 `--dest`를 다시 지정합니다. 기존 파일은 설치 위치의 `.bibi-skills-backups/`에 ZIP으로 남습니다. [전체 안내](../README.md)에서 두 도구 동시 설치와 유지보수 방법을 볼 수 있습니다.
