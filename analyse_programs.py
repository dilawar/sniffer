from compare import CompareProgram
from create_graph import CreateNetwork

# Let's get down to business.
plag = CompareProgram()
plag.traverse_and_compare()
plag.save_logs()

network = CreateNetwork()
network.open_stat_file()
network.create_network()
network.draw_and_save_grapgh()

