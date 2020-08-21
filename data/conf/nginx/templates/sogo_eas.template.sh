if printf "%s\n" "${SKIP_SOGO}" | grep -E '^([yY][eE][sS]|[yY])+$' >/dev/null; then
  echo "return 410;"
else
  echo "proxy_pass http://sogo:20000/SOGo/Microsoft-Server-ActiveSync;"
fi
