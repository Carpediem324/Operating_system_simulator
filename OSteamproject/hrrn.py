from scheduler import Scheduler


class HRRN(Scheduler):
    def run(self):
        cur_time = 0
        finish_processes_count = 0
        at_idx = 0
        sorted_processes = sorted(self.processes, key=lambda x: x.at)
        while finish_processes_count < self.process_count:
            # 현재 시간과 AT가 일치하는 프로세스를 대기열 큐에 넣어주기
            at_idx = self.enqueue_arrived_processes(sorted_processes, at_idx, cur_time)

            # history 기록하기
            self.record_history(self.ready_queue[:], self.cpus, self.processes)

            for cpu in self.cpus:
                # 만약 cpu의 일이 끝났으면, 끝난 프로세스의 output을 저장하고 cpu를 쉬게 한다.
                if cpu.is_finished():
                    print("process finished - cur_time:", cur_time, " p_id :", cpu.process.id)
                    cpu.process.calculate_finished_process(cur_time)
                    finish_processes_count += 1
                    cpu.set_idle()

                # 다음 프로세스(next process)를 선택한다. (대기열 큐 중 response ratio가 가장 높은 것)
                if cpu.is_idle():
                    if self.ready_queue:
                        max_response_ratio = float("-inf")
                        for process in self.ready_queue:
                            response_ratio = (process.wt + process.bt) / process.bt
                            if response_ratio > max_response_ratio:
                                max_response_ratio = response_ratio
                                next_process = process
                        self.ready_queue.remove(next_process)  # 선택한 프로세스를 대기열 큐에서 삭제
                        cpu.set_process(next_process)

            # ready_queue의 모든 프로세스의 WT를 1씩 추가
            for process in self.ready_queue:
                process.wt += 1

            # 현재 시간 1 증가
            cur_time += 1
            super().work()
