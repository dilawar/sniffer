import networkx as nx
import matplotlib.pyplot as plt
import os
import sys

class CreateGraph():

    def __init__(self, dir):
        self.dir = dir
        self.stat_dir = self.dir+'/stats/'
        self.stat_file = self.dir+'/stats/stats.log'
        self.file1 = []
        self.file2 = []
        self.user_dict = dict()
        self.user1 = []
        self.user2 = []
        self.ratio = []
        self.matches = []
        self.avg_match = []
    
    def open_stat_file(self):
        print self.stat_file
        if os.path.exists(self.stat_file):
            self.f = open(self.stat_file)
        else:
            print 'Stat file does not exists.'
            sys.exit(2)

    def create_network(self):
        self.create_lists()
        self.graph_low = nx.Graph()
        self.graph_high = nx.Graph()
        self.graph_med = nx.Graph()
        
        for i in self.user_dict :
            self.graph_low.add_node(self.user_dict[i], name=i)
            self.graph_high.add_node(self.user_dict[i], name = i)
            self.graph_med.add_node(self.user_dict[i], name = i)

        for i in range(len(self.ratio)):
            rat = self.ratio[i]
            
            if float(rat) >= 0.55 and float(rat) < 1.1:
                user1 = self.user1[i]
                user2 = self.user2[i]
                #print rat, user1, self.user_dict[user1], user2, self.user_dict[user2]
                self.graph_high.add_edge(self.user_dict[user1], \
                        self.user_dict[user2], weight=rat)

            if  float(rat) >= 0.35 :
                user1 = self.user1[i]
                user2 = self.user2[i]
                self.graph_med.add_edge(self.user_dict[user1],\
                        self.user_dict[user2], weight=rat, color='red')
            
            if float(rat) >= 0.17 :
                user1 = self.user1[i]
                user2 = self.user2[i]
                self.graph_low.add_edge(self.user_dict[user1],\
                        self.user_dict[user2], weight=rat, color='blue')



    def create_lists(self):
        self.open_stat_file()
        #print self.f.name
        for line in self.f :
            if len(line) > 2:
                [count, matches, avg_match, ratio, file1, file2] \
                        = line.split(',')
                self.file1.append(file1)
                self.file2.append(file2)
                self.ratio.append(ratio)
                self.matches.append(matches)
                self.avg_match.append(avg_match)
                user1 = file1.split(self.dir)[1]
                user2 = file2.split(self.dir)[1]
                u1 = user1.split('/')[1]
                u2 = user2.split('/')[1]

                self.user1.append(u1)
                self.user2.append(u2)
                
                if u1 in self.user_dict : pass 
                else :
                    self.user_dict[u1] = len(self.user_dict) + 1
                
                if u2 in self.user_dict : pass 
                else :
                    self.user_dict[u2] = len(self.user_dict) + 1

        #print self.user_dict
    
    def draw_and_save_grapgh(self):
        
        self.create_network()
        print '\n\n** Saving graphs in {0} **'.format(self.stat_dir)
        plt.figure(0)
        plt.subplot(311)
        plt.title('Possible interaction')
        fig = nx.draw_graphviz(self.graph_low \
                , prog='twopi' \
                , node_size= 80 \
                , font_size = 6  \
                , with_labels = True \
                , width = 0.5 \
                , node_color = 'yellow' \
                )
        
        plt.subplot(312)
        plt.title('Possible copies')
        nx.draw_graphviz(self.graph_med \
                , prog='fdp' \
                , node_size= 80 \
                , font_size = 6 \
                , with_labels = True \
                , width = 1.0 \
                , node_color = 'yellow' \
                )
        
        plt.subplot(313)
        plt.title('Definite copies')
        nx.draw_graphviz(self.graph_high \
                , prog='fdp' \
                , node_size= 80 \
                , font_size = 6 \
                , with_labels = True \
                , width = 1.9 \
                , node_color = 'yellow' \
                )
        plt.savefig(self.stat_dir+'/assignment.png')


        plt.figure(1)
        plt.title('Possible interactions')
        fig = nx.draw_graphviz(self.graph_low, prog='twopi')
        plt.savefig(self.stat_dir+'/low.png')
        
        plt.figure(2)
        plt.title('Possible copies')
        nx.draw_graphviz(self.graph_med, prog='twopi')
        plt.savefig(self.stat_dir+'/medium.png')
        
        plt.figure(3)
        plt.title('Definite copies')
        nx.draw_graphviz(self.graph_high, prog='twopi')
        plt.savefig(self.stat_dir+'/high.png')
