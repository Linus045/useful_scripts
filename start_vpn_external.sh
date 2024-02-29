# create netns
sudo ip netns add VPN

# setup eth link
sudo ip link add br_host_side type veth peer name br_vpn_side

# move vpn eth link into netns
sudo ip link set br_vpn_side netns test_vpn

# setup interface
sudo ip address add dev br_host_side local 10.0.0.1/24
sudo ip netns exec test_vpn ip address add dev br_vpn_side local 10.0.0.2/24
sudo ip netns exec test_vpn ip route add default via 10.0.0.1 dev br_vpn_side

# enable ip forwarding
echo "1" | sudo ip netns exec test_vpn tee /proc/sys/net/ipv4/ip_forward


sudo iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -o wlp2s0 -j MASQUERADE

sudo ip netns exec VPN vpnc homeserver
sudo ip netns exec VPN sudo -u linus firefox -P VPN


# DEBUGGING 
sudo ip netns exec test_vpn tcpdump --interface=br_vpn_side -f -n -vvv

# also make sure nftables is not blocking anything (especially the forward table)
sudoedit /etc/nftables.conf
