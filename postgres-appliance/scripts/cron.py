import time
from crontab import CronTab
import sys

def main():
  # check whether username is provided or not as an argument
  # if not current user is considered
  username = True if len(sys.argv) < 2 else sys.argv[1]

  # read all the crontabs from /var/spool/cron/crontabs/$username
  cron_tabs = CronTab(user=username)

  while True:
    # check for all the pending jobs and schedule it to run
    for job in cron_tabs:
      job.run_pending()
    time.sleep(60)

if __name__ == '__main__':
  main()
