trap 'kill 0' EXIT

cd application && npm run dev &
sleep 5 &
cd backend && python3 manage.py runserver 5500 &

wait