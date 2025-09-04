# pvmon

The [pv](https://codeberg.org/ivarch/pv) utility currently [does not support](https://codeberg.org/ivarch/pv/issues/12) watching multiple processes. Also, it [does not support](https://codeberg.org/ivarch/pv/src/commit/a629a488d7f1d07098caa2a6793e41a3f1088c8d/src/main/options.c#L742) using cursor positioning with the `-d`. This means there's no easy way to use it to monitor the parallel execution of multiple commands.

So, `pvmon` is a simple Python script that monitors a process name using `psutil` and, for each new process, calls `pv -d` on it while collating the carriage returns itself.

```
kuilin@kuilin-outb ~> sudo paste /dev/sda /dev/sdb > /dev/null &
kuilin@kuilin-outb ~> sudo paste /dev/sda > /dev/null &
kuilin@kuilin-outb ~> sudo pvmon paste
[1] 265591
   3:/dev/sda: 14.8GiB 0:00:12 [ 484MiB/s] [======>           ]   6% ETA 0:07:53
   4:/dev/sdb: 31.5MiB 0:00:12 [0.00  B/s] [>                 ]   0% ETA 0:00:00
[2] 265608
   3:/dev/sda: 13.5GiB 0:00:12 [ 541MiB/s] [=====>            ]   5% ETA 0:07:05
```
