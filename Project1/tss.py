# March 7, 2021
# Mizuki Hashimoto
#
# [Project 1]
# Create a simple time-sharing system using a round-robin selection algorithm.
# Processes will be loaded into the system all at once using an input file.
# Outputs an audit log that records process starting and ending times.
# All processes have equal priority. Fixed assumption is made for context switching time.
# Assume all processes fit into main memory.

# <input file format>
# number_of_processes quantum
# id1 time1
# id2 time2
#  :    :

# <output file format>
# Time Process_ID Log
# time1 id1 log1
# time2 id2 log2
#   :    :   :

import queue

class Process:
  def __init__(self, id, time):
    self.id = id
    self.time = time


# put processes into queue; get one process; 
# increment cpu time according to stated process time;
# subtract quantum from process time and put the process 
# back to queue if its process time exceeds quantum;
# repeat until queue get empty.
def round_robin(processes, quantum, audit_log):
  ready_queue = queue.Queue()

  for id, time in processes:
    ready_queue.put(Process(id, time))
  
  cpu_time = 0
  while not ready_queue.empty():
    cpu_time += 1  # overhead: run the dispatcher
    process = ready_queue.get()
    cpu_time += 1  # overhead: restore the new process's context before it can begin running
    audit_log += f'{cpu_time:>5} |{process.id:>11} | Process start\n'
    
    if process.time > quantum:
      cpu_time += quantum  # used up quantum; it's time to swap the process
      process.time -= quantum  # = remaining process time
      cpu_time += 1  # overhead: save the running process's context
      ready_queue.put(process)  # put unfinished process back to queue
      audit_log += f'{cpu_time:>5} |{process.id:>11} | Process unfinished within the quantum. Still need {process.time} to complete\n'
    else:
      cpu_time += process.time
      audit_log += f'{cpu_time:>5} |{process.id:>11} | Process complete\n'
  
  audit_log += f'\nAll processes completed in {cpu_time}'
  
  return audit_log

def main():
  # open input file, read number of processes, quantum, and processes (id, time);
  # prepare audit log.
  with open('input.txt', 'r') as input_file:
    audit_log = f'{"Time":>5} {"Process ID":>12} {"Log":>5}\n\n'

    num_process, quantum = map(int, input_file.readline().split())
    processes = []
    for i in range(num_process):
      id, time = input_file.readline().split()
      processes.append([id, int(time)])
    
    audit_log = round_robin(processes, quantum, audit_log)

  # open output file, write audit log.
  with open('audit_log.txt', 'w') as output_file:
    output_file.write(audit_log)

  print(audit_log)  # console output looks better than Windows txt file output.

if __name__ == '__main__':
  main()