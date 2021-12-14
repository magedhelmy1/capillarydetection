# nginx

For optimum performance create the following file `/etc/sysctl.d/99-tuning.conf` and add these items:

```
net.ipv4.ip_local_port_range='1024 65535'
net.ipv4.tcp_tw_reuse='1'
net.ipv4.tcp_fin_timeout='15'
net.core.netdev_max_backlog='4096'
net.core.rmem_max='16777216'
net.core.somaxconn='4096'
net.core.wmem_max='16777216'
net.ipv4.tcp_max_syn_backlog='20480'
net.ipv4.tcp_max_tw_buckets='400000'
net.ipv4.tcp_no_metrics_save='1'
net.ipv4.tcp_rmem='4096 87380 16777216'
net.ipv4.tcp_syn_retries='2'
net.ipv4.tcp_synack_retries='2'
net.ipv4.tcp_wmem='4096 65536 16777216'
vm.min_free_kbytes='65536'
```

After saving the file apply the new settings with `sysctl -p`.

Also run the following to update limits in the OS:

```bash
ulimit -n 1048576
```
