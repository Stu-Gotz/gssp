#!/usr/bin/env bash
cleanup() {
  trap - INT TERM EXIT   # don't run cleanup twice
  kill 0                 # stop everything this script started
}
trap cleanup INT TERM EXIT

cd application && npm run dev &
sleep 5 &
cd backend && python3 manage.py runserver 5500 &

wait