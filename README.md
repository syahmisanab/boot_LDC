sudo apt install guvcview v4l-utils ffmpeg -y

chromium-browser   --use-fake-ui-for-media-stream   --autoplay-policy=no-user-gesture-required   --enable-features=WebRTCPipeWireCapturer   https://teachablemachine.withgoogle.com

chromium-browser \
  --disable-features=WebRTCPipeWireCapturer \
  --use-fake-ui-for-media-stream \
  --autoplay-policy=no-user-gesture-required \
  https://teachablemachine.withgoogle.com

sudo apt install v4l-utils ffmpeg


sudo apt install -y pipewire wireplumber xdg-desktop-portal xdg-desktop-portal-gtk v4l-utils

