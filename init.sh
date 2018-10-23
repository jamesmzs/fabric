#!/bin/bash
#for init-os
#关闭防火墙,内核参数调整,超级用户权限

dir=`dirname $0`

. $dir/config

function step_1() 
{
  sed -i 's/SELINUX=enforcing/SELINUX=disabled/'  $selinux
  systemctl stop $iptables 
  systemctl disable $iptables

  echo "$user    ALL=(ALL)       ALL" >> $file
}


function step_2()
{
cat << EOF >> $sysctlfile
net.ipv6.conf.all.disable_ipv6 = 1 
net.ipv6.conf.default.disable_ipv6 = 1
net.ipv4.tcp_tw_recycle = 1
net.ipv4.tcp_tw_reuse = 1
net.ipv4.ip_local_port_range = 1024    65000
net.ipv4.icmp_ignore_bogus_error_responses = 1
vm.max_map_count = 655360
EOF
sysctl -p
}

function step_3()
{
cat << EOF >> $nofile
* soft nofile 65535
* hard nofile 65535
* soft nproc 65535
* hard nproc 65535

EOF
}

main()
{
  step_1
  step_2
  step_3
}

main

