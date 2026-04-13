# OpenClaw 설치 및 초기 설정 가이드 (초보자용, 한국어)

## 개요

**OpenClaw는 “메신저로 대화하면 실제 컴퓨터 작업까지 수행하는 오픈소스 개인 AI 어시스턴트”입니다.**

- 할 수 있는 일(요약): 채팅 채널(WhatsApp/Telegram/Discord 등)에서 요청을 받아, 게이트웨이(핵심 서비스)를 통해 도구 실행/자동화/응답을 처리합니다.

> **표기 규칙**
> - **공식 문서 기준**: 공식 사이트/공식 문서에서 직접 확인된 내용
> - **추가 설명**: 이해를 돕는 보조 설명(절차 근거로 사용하지 않음)
> - **추정 불가/확인 필요**: 공식 문서에서 현재 명확히 확인되지 않은 항목

---

## 설치 전 준비

### 1) 요구사항 확인

- **무엇을 하는 단계인지**: 설치 가능한 운영체제/런타임 조건을 먼저 점검합니다.
- **왜 필요한지**: 요구사항이 맞지 않으면 설치 스크립트가 실패하거나 이후 게이트웨이가 불안정해질 수 있습니다.

**공식 문서 기준**
- Node.js: **Node 24 권장**, **Node 22.14+ 지원**
- 운영체제: macOS / Linux / Windows 지원
- Windows: **WSL2 경로를 더 안정적인 권장 경로**로 안내
- 선택 사항: Brave Search API(웹 검색 기능 활성화 시)

**추가 설명**
- 나무위키 등 커뮤니티 문서에서도 “권한이 큰 도구이므로 운영 환경 분리”를 자주 언급합니다. 다만 설치 절차의 기준은 반드시 공식 문서로 잡으세요.

**추정 불가/확인 필요**
- CPU/RAM 최소 사양의 고정 기준은 공식 설치 페이지에서 명시적으로 확인되지 않았습니다.

---

## 설치

## 2) 가장 빠른 시작 방법

- **무엇을 하는 단계인지**: OpenClaw 대시보드를 즉시 띄워 동작 여부를 확인합니다.
- **왜 필요한지**: 설치 직후 “실행 경로가 열렸는지”를 가장 빠르게 검증할 수 있습니다.

**공식 문서 기준**
```bash
openclaw dashboard
```

- 대시보드 기본 주소: `http://127.0.0.1:18789/`

> 참고: 이 명령은 `openclaw` CLI가 설치되어 있어야 동작합니다.

---

### 3) Windows 기준 권장 흐름 (WSL2 권장)

#### 3-1) WSL2 설치 (권장)
- **무엇**: Windows에 Linux 실행 환경(WSL2)을 준비합니다.
- **왜**: 공식 문서에서 WSL2를 “더 안정적인 전체 경험” 경로로 안내합니다.

**공식 문서 기준 (PowerShell, 관리자)**
```powershell
wsl --install
# 또는 배포판 지정
wsl --list --online
wsl --install -d Ubuntu-24.04
```

#### 3-2) (WSL 내부) OpenClaw 설치
- **무엇**: WSL2의 Linux 셸에서 OpenClaw를 설치합니다.
- **왜**: CLI/Gateway/도구 호환성이 가장 높은 권장 경로입니다.

**공식 문서 기준 (WSL 터미널)**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

---

### 4) macOS/Linux 공통 흐름

- **무엇**: 공식 원라이너 설치 스크립트로 OpenClaw를 설치합니다.
- **왜**: OS 감지, Node 설치(필요 시), OpenClaw 설치, 온보딩 진입까지 자동화됩니다.

**공식 문서 기준**
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

---

### 5) Windows 네이티브 대안 흐름

- **무엇**: PowerShell에서 Windows 전용 설치 스크립트를 실행합니다.
- **왜**: WSL2를 쓰지 않는 환경에서도 설치 자체는 가능합니다.

**공식 문서 기준 (PowerShell)**
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

**추가 설명**
- 네이티브 Windows도 지원되지만, 공식 문서는 여전히 WSL2를 더 안정적인 경로로 권장합니다.

---

## 초기 설정

### 6) onboard(초기 설정) 실행

- **무엇을 하는 단계인지**: 설정 마법사로 게이트웨이/인증/채널/데몬을 한 번에 설정합니다.
- **왜 필요한지**: 수동 설정 실수를 줄이고, 바로 운영 가능한 기본 상태를 만듭니다.

**공식 문서 기준**
```bash
openclaw onboard --install-daemon
```

#### onboard에서 설정하는 핵심 항목

1. **게이트웨이**
   - 무엇: 로컬/원격 게이트웨이 유형 선택
   - 왜: 메시지 처리의 중심 서비스 위치를 결정
2. **인증 방식**
   - 무엇: OpenAI(OAuth/API 키) 또는 Anthropic(API 키 권장, `claude setup-token` 지원) 등 설정
   - 왜: 실제 모델 호출 권한이 있어야 응답 가능
3. **채팅 플랫폼 연동**
   - 무엇: WhatsApp QR, Telegram/Discord 토큰 등 연결
   - 왜: 사용자와 대화할 입출력 채널이 필요
4. **daemon 설치 개념**
   - 무엇: 백그라운드 서비스(자동 시작)로 게이트웨이 등록
   - 왜: 터미널을 닫아도 안정적으로 계속 동작
   - 플랫폼 예시(공식 문서): macOS `launchd`, Linux/WSL2 `systemd`, Windows는 Scheduled Task 우선

---

### 7) 주요 설정 파일/디렉토리 위치

- **무엇을 하는 단계인지**: 설정/인증 파일 위치를 파악합니다.
- **왜 필요한지**: 백업, 이전, 문제 진단 시 가장 먼저 확인해야 합니다.

**공식 문서 기준**
- 기본 구성 디렉토리: `~/.openclaw/`
- OAuth 자격 증명: `~/.openclaw/credentials/oauth.json`
- 인증 프로필: `~/.openclaw/agents/<agent>/agent/auth-profiles.json`
- WhatsApp 자격 증명(예): `~/.openclaw/credentials/whatsapp/`

**추가 설명**
- 헤드리스 서버에서는 브라우저가 있는 머신에서 OAuth를 먼저 완료한 뒤 `oauth.json`을 서버로 옮기는 방법을 공식 가이드가 제시합니다.

---

## 실행 및 연결

### 8) 게이트웨이 시작 및 상태 확인

- **무엇을 하는 단계인지**: 게이트웨이 실행 여부와 헬스를 확인합니다.
- **왜 필요한지**: 채널 연결/메시지 응답의 전제조건이 게이트웨이 정상 상태이기 때문입니다.

**공식 문서 기준**
```bash
openclaw gateway status
openclaw gateway --port 18789
openclaw status
openclaw health
openclaw security audit --deep
```

---

### 9) 채팅 플랫폼 연결 방식

#### 9-1) WhatsApp
- **무엇**: QR 코드로 WhatsApp Web 세션을 연결
- **왜**: OpenClaw가 WhatsApp 메시지를 송수신하려면 계정 링크가 필요

**공식 문서 기준**
```bash
openclaw channels login --channel whatsapp
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

**공식 문서 기준 (운영 권장)**
- 가능하면 **전용 전화번호 사용 권장**
- 기본 DM 정책은 pairing(미승인 발신자는 승인 전 처리 불가)

#### 9-2) Telegram
- **무엇**: BotFather에서 봇 토큰 생성 후 설정
- **왜**: Telegram은 토큰 기반 인증으로 게이트웨이에 붙습니다.

**공식 문서 기준**
```bash
# 토큰 설정 후
openclaw gateway
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
```

> 참고: Telegram은 `openclaw channels login telegram` 방식이 아니라 토큰 설정 방식입니다.

#### 9-3) Discord
- **무엇**: Discord Developer Portal에서 봇 생성/토큰 발급 후 연결
- **왜**: Discord Bot API 기반으로 게이트웨이가 DM/서버 채널을 처리합니다.

**공식 문서 기준**
```bash
export DISCORD_BOT_TOKEN="YOUR_BOT_TOKEN"
openclaw config set channels.discord.token --ref-provider default --ref-source env --ref-id DISCORD_BOT_TOKEN
openclaw config set channels.discord.enabled true --strict-json
openclaw gateway
openclaw pairing list discord
openclaw pairing approve discord <CODE>
```

---

## 점검 방법

### 10) 설치 후 정상 동작 확인

- **무엇을 하는 단계인지**: CLI/게이트웨이/메시지 전송까지 최소 E2E를 확인합니다.
- **왜 필요한지**: “설치만 된 상태”와 “실제로 채널에서 동작하는 상태”를 구분하기 위해서입니다.

**공식 문서 기준**
```bash
openclaw --version
openclaw doctor
openclaw gateway status
openclaw health
```

테스트 메시지:
```bash
openclaw message send --target +15555550123 --message "Hello from OpenClaw"
```

---

## 문제 해결

### 11) 보안/운영 시 주의사항

**공식 문서 기준**
- pairing 승인 전에는 미승인 DM이 처리되지 않음(기본 보안 장치)
- 토큰/API 키는 환경변수/SecretRef 기반 관리 권장
- 게이트웨이는 상시 실행 서비스(daemon)로 관리 권장
- WhatsApp은 전용 번호 운영 권장

**추가 설명**
- OpenClaw는 실제 작업을 수행하므로, 운영 계정/채널 권한 범위를 최소화하는 것이 안전합니다.

**추정 불가/확인 필요**
- 특정 기업 보안정책(예: 어떤 산업에서 금지/허용)은 공식 설치 문서 범위 밖이므로 조직별 보안팀 기준으로 별도 검토가 필요합니다.

---

### 12) 문제 발생 시 먼저 점검할 항목 (자주 막히는 포인트)

1. `openclaw` 명령이 인식되지 않음  
   - PATH 문제 가능성 → `npm prefix -g` / PATH 점검
2. `openclaw health`에서 auth 미설정 표시  
   - `openclaw onboard --install-daemon`로 인증 단계 재진입
3. Telegram/Discord가 무응답  
   - 토큰 설정 유무, 게이트웨이 실행 상태, pairing 승인 여부 확인
4. WhatsApp 전송 실패  
   - 채널 로그인 상태(`openclaw channels status`), pairing 코드 승인 여부 확인
5. Windows 네이티브에서 불안정  
   - 공식 권장 경로인 WSL2로 전환 검토

점검 체크리스트:
- [ ] `openclaw --version` 정상 출력
- [ ] `openclaw doctor` 치명 오류 없음
- [ ] `openclaw gateway status`가 running/정상
- [ ] 대상 채널(WhatsApp/Telegram/Discord) 토큰 또는 QR 연결 완료
- [ ] pairing 승인 완료
- [ ] 테스트 메시지 송수신 성공

---

## 요약

### 13) 처음 설치하는 사람용 최소 실행 순서

1. (Windows면) 가능하면 WSL2 설치 후 WSL 터미널 사용
2. 설치 스크립트 실행
3. `openclaw onboard --install-daemon` 실행
4. 인증(OpenAI/Anthropic 등) + 채널(WhatsApp/Telegram/Discord) 연결
5. `openclaw gateway status` / `openclaw health` 확인
6. `openclaw message send ...`로 테스트

---

## 복붙용 최소 명령어 모음

### macOS / Linux / WSL2
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
openclaw onboard --install-daemon
openclaw gateway status
openclaw health
openclaw dashboard
```

### Windows (PowerShell, 네이티브 대안)
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
openclaw onboard --install-daemon
openclaw gateway status
openclaw health
```

### WhatsApp 연결
```bash
openclaw channels login --channel whatsapp
openclaw pairing list whatsapp
openclaw pairing approve whatsapp <CODE>
```

### Telegram/Discord pairing 확인
```bash
openclaw pairing list telegram
openclaw pairing approve telegram <CODE>
openclaw pairing list discord
openclaw pairing approve discord <CODE>
```

---

## 참고 링크

### 공식(우선 출처)
- https://openclaw.ai/
- https://open-claw.me/ko/guide/getting-started
- https://docs.openclaw.ai/install
- https://docs.openclaw.ai/platforms/windows
- https://docs.openclaw.ai/channels/whatsapp
- https://docs.openclaw.ai/channels/telegram
- https://docs.openclaw.ai/channels/discord

### 보조 설명(개념 참고)
- https://namu.wiki/w/OpenClaw

---

**주의: 공식 문서가 업데이트되면 명령어나 절차가 바뀔 수 있음.**
