# pvmon

The [pv](https://codeberg.org/ivarch/pv) utility currently [does not support](https://codeberg.org/ivarch/pv/issues/12) watching multiple processes. Also, it [does not support](https://codeberg.org/ivarch/pv/src/commit/a629a488d7f1d07098caa2a6793e41a3f1088c8d/src/main/options.c#L742) using cursor positioning with the `-d`. This means there's no easy way to use it to monitor the parallel execution of multiple commands.

So, `pvmon` is a simple Python script that monitors a process name using `psutil` and, for each new process, calls `pv -d` on it while collating the carriage returns itself.
