#!/usr/bin/env bash
# Đẩy commit lên GitHub, tự gộp khi có người đẩy cùng lúc.
# Tệp sinh tự động (rss.xml, sitemap*.xml) lấy bản trên GitHub rồi tạo lại; xung đột khác giữ bản mới của bot.
# Tham số: lệnh tạo lại tệp sau khi gộp (có thể bỏ trống).
REGEN="$1"
for i in 1 2 3 4 5; do
  if ! git pull --rebase -q; then
    git checkout --ours rss.xml sitemap*.xml 2>/dev/null; git add rss.xml sitemap*.xml 2>/dev/null
    U=$(git diff --name-only --diff-filter=U)
    if [ -n "$U" ]; then git checkout --theirs -- $U; git add -- $U; fi
    GIT_EDITOR=true git rebase --continue || { git rebase --abort; exit 1; }
    if [ -n "$REGEN" ]; then
      bash -c "$REGEN" && git add -A
      git diff --cached --quiet || git commit -q -m "Tạo lại sơ đồ trang và RSS sau khi gộp"
    fi
  fi
  git push -q && exit 0
  sleep $((i*8))
done
exit 1
