# Claude Code용 스킬

| 스킬 | 설명 |
|---|---|
| [korean-writing](korean-writing/SKILL.md) | 사실과 말투를 보존하는 한국어 리라이팅 |
| [pm-frame](pm-frame/SKILL.md) | 문제 정의부터 결정문까지 이어지는 6단계 PM 프레임 |

각 폴더에 `SKILL.md`와 참고 문서가 들어 있습니다. Codex판과 같은 편집·판단 기준을 사용하며 Claude Code의 슬래시 명령으로 호출합니다.

## 개인 설치

저장소 루트에서 실행합니다.

```bash
python3 scripts/install.py --target claude-code
```

기본 설치 위치는 `~/.claude/skills/`입니다. 하나만 설치하려면 `--skill korean-writing` 또는 `--skill pm-frame`을 붙입니다.

## 프로젝트에만 설치

```bash
python3 scripts/install.py --target claude-code --dest /path/to/project/.claude/skills
```

`/path/to/project`를 실제 대상 프로젝트 경로로 바꿉니다. 스크립트가 필요 없으면 `korean-writing/` 또는 `pm-frame/` 폴더 전체를 대상 skills 폴더로 복사해도 됩니다. 참고 문서도 함께 있어야 합니다.

## 호출

```text
/korean-writing 이 이메일의 요청과 기한을 유지하면서 자연스럽게 다듬어줘.

/pm-frame 이 기획의 문제 정의부터 한 번에 하나씩 질문해줘.
```

요청 내용에 따른 자동 선택도 사용할 수 있습니다. 설치 후 `/` 목록에서 스킬 이름을 확인하세요. 목록에 보이지 않으면 새 세션을 시작해 다시 확인합니다.

이 안내는 로컬 Claude Code용입니다. 개인·프로젝트 설치 위치와 적용 범위는 [Claude Code 공식 스킬 문서](https://code.claude.com/docs/en/skills)를 참고하세요.

## 업데이트

```bash
git pull --ff-only
python3 scripts/install.py --target claude-code --replace
```

사용자 지정 위치에 설치했다면 같은 `--dest`를 다시 지정합니다. 기존 파일은 설치 위치의 `.bibi-skills-backups/`에 ZIP으로 남습니다. 스킬 자체가 심볼릭 링크이면 스크립트가 멈추므로, 그 경우 링크가 가리키는 원본 위치를 확인해 관리하세요.

이 폴더는 `codex/`의 편집 원본에서 `scripts/sync_claude.py`로 생성됩니다. 공통 내용의 수정·기여 방법은 [전체 안내](../README.md)를 참고하세요.
