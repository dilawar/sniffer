import re


data1 = '''component sim_ex_inertial_transport is
port(	a_in: in bit;
	c_inertial_out, c_transport_out: out bit
);
end component;'''

data = '''component FA_8 is
port(a: in bit_vector(7 downto 0);
	b: in bit_vector(7 downto 0);
	s: out bit_vector(7 downto 0);
	c: out bit);
end component;'''
#
#m = re.search(r'''component\s+(\w+)\s+is\s+
#                port\s*[(]
#               ((\s*\w+[:]\s*(in|out)\s+\w+([(]\d+\s+\w+\s+\d+[)])*[;]*)+[)]\s*[;])
#                \s+end\s+component\s*\w*[;]''', data, re.I | re.VERBOSE)
#
#
#if m:
#   # print m.group(0)
#   # print m.group(1)
#   # print m.group(2)
#    pass
#

data3 = '''component HA
port (a,c:in bit;sum,carry:out bit);
end component;'''

data4 = '''component full_adder 
 port (a,b,c_in :in bit ; s_out,c_out : out bit) ;
  end component ;'''

data5 = '''component coach
port(d: in bit_vector (9 downto 0); o: out bit_vector (7 downto 0));
end component;'''

m = re.search(r'''component\s+(\w+)\s*(is)*\s+
                port\s*[(]
                (\s*\w+(\s*[,]\s*\w+\s*)*\s*[:]\s*
                (in|out)\s*\w+\s*([(]\s*\d+\s*\w+\s*\d+\s*[)])*\s*[;]*)*
                \s*[)]\s*[;]
                \s+end\s+component\s*\w*[;]'''
                , data5, re.I | re.VERBOSE)

if m:
    print m.group(0)
else:
    print "Cant find pattern"
