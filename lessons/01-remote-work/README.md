# 01 · 원격 작업하기

로컬 컴퓨터 ↔ Tailscale ↔ Jetson의 OpenSSH를 연결하고 `ssh jetson`으로 접속합니다. GUI 작업에는 RustDesk를 쓸 수 있습니다.

Python 3.10 이상과 OpenSSH client. 이 저장소는 비밀키, 실제 장치 주소, 로그인 token을 포함하지 않습니다. 예제와 점검 코드만 담았습니다.

```bash
python3 check_config.py ssh_config.example
```

`ssh -G -F`로 config 해석만 확인합니다. 네트워크 접속, key 생성, package 설치, login 또는 ~/.ssh/config 변경을 자동으로 하지 않습니다.

## 직접 설정하는 순서

1. **Jetson**에서 `sudo apt install openssh-server`, `sudo systemctl enable --now ssh`. `whoami`로 계정 이름 확인.
2. **두 장치**에 [Tailscale](https://tailscale.com/download)을 설치하고 같은 tailnet에 로그인. Linux는 공식 설치 후 `sudo tailscale up`을 사용. `tailscale ip -4`로 Jetson 주소 확인.
3. **로컬**에서 `ssh-keygen -t ed25519 -a 64 -f ~/.ssh/id_ed25519_jetson -C mero-jetson`으로 key pair 생성. Passphrase 사용, 기존 key 덮어쓰기 금지.
4. 첫 연결 때 Jetson의 `sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub` 결과와 host fingerprint 비교.
5. **로컬**에서 `ssh-copy-id -i ~/.ssh/id_ed25519_jetson.pub USER@TAILSCALE_IP`. 개인키는 보내지 않고 .pub만 등록.
6. `ssh_config.example`의 User/IP를 바꿔 로컬 ~/.ssh/config에 **추가**. Linux/macOS: `chmod 600 ~/.ssh/config`. `ssh -G jetson` 확인 후 `ssh jetson` 접속.
7. `hostname`, `whoami`, `pwd`로 Jetson shell 확인. `scp example.py jetson:~/`로 복사 가능.

이 구성은 일반 OpenSSH over Tailscale입니다. 별도 Tailscale SSH 기능(`tailscale up --ssh`)은 사용하지 않습니다.

Windows의 config는 `$HOME/.ssh/config`이며 확장자가 없습니다. ssh-copy-id가 없으면 PowerShell에서:

```powershell
Get-Content "$HOME/.ssh/id_ed25519_jetson.pub" | ssh USER@TAILSCALE_IP "umask 077; mkdir -p ~/.ssh; cat >> ~/.ssh/authorized_keys"
```

GUI가 필요하면 두 장치에 아키텍처가 맞는 [RustDesk](https://rustdesk.com/docs/en/client/)를 설치하고 상대 ID와 승인/비밀번호로 접속합니다. Jetson ARM64와 Linux display 지원을 확인합니다. Tailscale direct-IP 연결은 [공식 안내](https://tailscale.com/docs/solutions/access-remote-desktops-with-rustdesk)를 참고하세요.

## 검증 범위

Config 예제를 로컬 OpenSSH로 해석했습니다. 신규 실제 Jetson, Tailscale 계정 로그인과 RustDesk 원격 화면 연결은 수행하지 않았습니다. 본인 장치와 권한으로 사이트 강의를 따라 설정하세요.
