import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import socket
import ssl
import urllib.request
import urllib.parse
import re
import json
import threading
import webbrowser
from datetime import datetime
import time
import os
import sys
import subprocess
import platform
from concurrent.futures import ThreadPoolExecutor, as_completed
import http.client
import ssl
import email
import base64

class UltraFastWebsiteHunter:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Ultra Fast Website Info Hunter Pro")
        self.root.geometry("1300x850")
        self.root.configure(bg='#0a0a0a')
        
        # Dark theme colors
        self.bg_dark = '#0a0a0a'
        self.bg_medium = '#1a1a1a'
        self.bg_light = '#2a2a2a'
        self.bg_input = '#1e1e1e'
        self.text_primary = '#ffffff'
        self.text_secondary = '#b3b3b3'
        self.accent_blue = '#0078d4'
        self.accent_green = '#4caf50'
        self.accent_red = '#f44336'
        self.accent_yellow = '#ff9800'
        self.accent_purple = '#9c27b0'
        self.accent_cyan = '#00bcd4'
        
        # Performance optimization
        self.scan_cache = {}
        self.timeout = 3
        self.thread_pool = ThreadPoolExecutor(max_workers=15)
        
        # WHOIS servers database (complete list)
        self.whois_servers = {
            'com': 'whois.verisign-grs.com',
            'net': 'whois.verisign-grs.com',
            'org': 'whois.pir.org',
            'info': 'whois.afilias.net',
            'biz': 'whois.neulevel.biz',
            'us': 'whois.nic.us',
            'uk': 'whois.nic.uk',
            'ca': 'whois.cira.ca',
            'de': 'whois.denic.de',
            'fr': 'whois.nic.fr',
            'au': 'whois.auda.org.au',
            'ru': 'whois.tcinet.ru',
            'jp': 'whois.jprs.jp',
            'cn': 'whois.cnnic.cn',
            'br': 'whois.registro.br',
            'in': 'whois.registry.in',
            'io': 'whois.nic.io',
            'co': 'whois.nic.co',
            'me': 'whois.nic.me',
            'tv': 'whois.nic.tv',
            'cc': 'whois.nic.cc',
            'xyz': 'whois.nic.xyz',
            'online': 'whois.nic.online',
            'site': 'whois.nic.site',
            'top': 'whois.nic.top',
            'club': 'whois.nic.club',
            'shop': 'whois.nic.shop',
            'blog': 'whois.nic.blog',
            'app': 'whois.nic.google',
            'dev': 'whois.nic.google',
        }
        
        # Hosting providers database
        self.hosting_providers = {
            'amazonaws.com': 'Amazon AWS',
            'googleusercontent.com': 'Google Cloud',
            'azure.com': 'Microsoft Azure',
            'digitalocean.com': 'DigitalOcean',
            'linode.com': 'Linode',
            'godaddy.com': 'GoDaddy',
            'secureserver.net': 'GoDaddy',
            'hostgator.com': 'HostGator',
            'websitewelcome.com': 'HostGator',
            'bluehost.com': 'Bluehost',
            'unifiedlayer.com': 'Bluehost',
            'siteground.com': 'SiteGround',
            'dreamhost.com': 'DreamHost',
            'a2hosting.com': 'A2 Hosting',
            'inmotionhosting.com': 'InMotion Hosting',
            'wpengine.com': 'WP Engine',
            'kinsta.com': 'Kinsta',
            'cloudflare.com': 'Cloudflare',
            'akamai.com': 'Akamai',
            'ovh.com': 'OVH',
            'hetzner.com': 'Hetzner',
            'vultr.com': 'Vultr',
            'choopa.com': 'Vultr',
            'namecheaphosting.com': 'Namecheap',
            'hostinger.com': 'Hostinger',
            'ipage.com': 'iPage',
            'liquidweb.com': 'Liquid Web',
            'rackspace.com': 'Rackspace',
            'alibabacloud.com': 'Alibaba Cloud',
            'oraclecloud.com': 'Oracle Cloud',
            'softlayer.com': 'IBM Cloud',
            'fastly.com': 'Fastly',
            'stackpath.com': 'StackPath',
            'bunnycdn.com': 'BunnyCDN',
        }
        
        self.setup_ui()
        
    def setup_ui(self):
        """Setup UI"""
        self.root.bind('<Return>', lambda event: self.start_scan())
        
        main_container = tk.Frame(self.root, bg=self.bg_dark)
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header
        header_frame = tk.Frame(main_container, bg=self.bg_dark)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        
        tk.Label(header_frame, text="⚡ Ultra Fast Website Info Hunter Pro",
                font=('Segoe UI', 24, 'bold'),
                bg=self.bg_dark, fg=self.accent_cyan).pack()
        
        tk.Label(header_frame,
                text="Advanced WHOIS Bypass | Hosting Detection | Full Intelligence | DEVELOP BY CHOWDHURY-VAI",
                font=('Segoe UI', 10),
                bg=self.bg_dark, fg=self.text_secondary).pack()
        
        # URL Input
        input_frame = tk.Frame(main_container, bg=self.bg_medium, relief='flat', bd=1)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        input_inner = tk.Frame(input_frame, bg=self.bg_medium)
        input_inner.pack(padx=15, pady=12, fill=tk.X)
        
        url_row = tk.Frame(input_inner, bg=self.bg_medium)
        url_row.pack(fill=tk.X)
        
        tk.Label(url_row, text="🎯 URL:", font=('Segoe UI', 11, 'bold'),
                bg=self.bg_medium, fg=self.accent_cyan).pack(side=tk.LEFT, padx=(0, 10))
        
        self.url_entry = tk.Entry(url_row, font=('Consolas', 12),
                                 bg=self.bg_input, fg=self.text_primary,
                                 insertbackground=self.accent_cyan,
                                 relief='flat', bd=8)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.url_entry.insert(0, "https://www.example.com")
        
        # Buttons
        btn_row = tk.Frame(input_inner, bg=self.bg_medium)
        btn_row.pack(fill=tk.X, pady=(10, 0))
        
        self.scan_btn = tk.Button(btn_row, text="⚡ FAST SCAN",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg=self.accent_blue, fg='white',
                                 activebackground='#0056b3',
                                 relief='flat', padx=20, pady=6,
                                 cursor='hand2', command=self.start_scan)
        self.scan_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        self.deep_btn = tk.Button(btn_row, text="🔍 DEEP SCAN (WHOIS BYPASS)",
                                 font=('Segoe UI', 10, 'bold'),
                                 bg=self.accent_purple, fg='white',
                                 activebackground='#7b1fa2',
                                 relief='flat', padx=20, pady=6,
                                 cursor='hand2', command=self.start_deep_scan)
        self.deep_btn.pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Button(btn_row, text="🗑️ CLEAR",
                 font=('Segoe UI', 10),
                 bg='#555555', fg='white',
                 relief='flat', padx=20, pady=6,
                 cursor='hand2', command=self.clear_results).pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Button(btn_row, text="🌐 OPEN",
                 font=('Segoe UI', 10),
                 bg=self.accent_green, fg='white',
                 relief='flat', padx=20, pady=6,
                 cursor='hand2', command=self.open_browser).pack(side=tk.LEFT, padx=(0, 8))
        
        tk.Button(btn_row, text="📊 EXPORT",
                 font=('Segoe UI', 10),
                 bg=self.accent_yellow, fg='black',
                 relief='flat', padx=20, pady=6,
                 cursor='hand2', command=self.export_report).pack(side=tk.LEFT)
        
        # Progress
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(input_inner, variable=self.progress_var,
                                       maximum=100, mode='determinate')
        self.progress.pack(fill=tk.X, pady=(10, 0))
        
        self.status_var = tk.StringVar(value="● Ready - Fast Scan or Deep Scan with WHOIS Bypass")
        tk.Label(input_inner, textvariable=self.status_var,
                font=('Segoe UI', 9), bg=self.bg_medium, fg=self.text_secondary).pack(anchor=tk.W, pady=(5, 0))
        
        # Notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        self.tabs = {}
        tab_names = [
            ('hosting', '🏢 Hosting & IP'),
            ('dns', '📡 DNS Records'),
            ('headers', '📨 Headers'),
            ('tech', '⚙️ Technologies'),
            ('security', '🔒 Security'),
            ('whois', '📋 WHOIS (Privacy Bypass)')
        ]
        
        for tab_id, tab_title in tab_names:
            frame = tk.Frame(self.notebook, bg=self.bg_medium)
            self.notebook.add(frame, text=f"  {tab_title}  ")
            self.tabs[tab_id] = self.create_text_widget(frame)
        
        # Status bar
        status_frame = tk.Frame(main_container, bg=self.bg_light, height=30)
        status_frame.pack(fill=tk.X, pady=(15, 0))
        status_frame.pack_propagate(False)
        
        tk.Label(status_frame, text="DEVELOP BY: CHOWDHURY-VAI | FB: facebook.com/itbossusa | WHOIS BYPASS TECHNOLOGY",
                font=('Segoe UI', 9, 'bold'), bg=self.bg_light, fg=self.accent_cyan,
                anchor=tk.CENTER).pack(expand=True)
        
    def create_text_widget(self, parent):
        """Create text widget"""
        frame = tk.Frame(parent, bg=self.bg_medium)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_widget = scrolledtext.ScrolledText(frame,
                                               font=('Consolas', 10),
                                               bg=self.bg_input,
                                               fg=self.text_primary,
                                               relief='flat',
                                               wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        for tag, color in [
            ('header', '#4fc3f7'), ('subheader', '#ce93d8'),
            ('success', '#66bb6a'), ('error', '#ef5350'),
            ('warning', '#ffa726'), ('info', '#42a5f5'),
            ('highlight', '#ffd54f'), ('critical', '#ff1744'),
            ('bypass', '#00e676'), ('hidden', '#ff9100')
        ]:
            text_widget.tag_config(tag, foreground=color)
            
        return text_widget
    
    def whois_query(self, domain, server=None):
        """Direct WHOIS query with smart fallback"""
        results = {}
        
        # Try multiple WHOIS methods
        methods = [
            self._whois_socket_direct,
            self._whois_http_api,
            self._whois_rdap_lookup,
            self._whois_history_check,
            self._whois_dns_trick,
            self._whois_hosting_leak
        ]
        
        with ThreadPoolExecutor(max_workers=len(methods)) as executor:
            futures = {executor.submit(method, domain): method.__name__ for method in methods}
            for future in as_completed(futures):
                method_name = futures[future]
                try:
                    result = future.result()
                    if result:
                        results[method_name] = result
                except:
                    pass
        
        return results
    
    def _whois_socket_direct(self, domain):
        """Direct WHOIS socket connection with referral following"""
        try:
            tld = domain.split('.')[-1].lower()
            whois_server = self.whois_servers.get(tld, 'whois.iana.org')
            
            # First query
            response = self._whois_raw_query(domain, whois_server)
            
            # Follow referrals
            referral = re.search(r'Whois Server:\s*(\S+)', response, re.IGNORECASE)
            if referral:
                referral_server = referral.group(1)
                if referral_server != whois_server:
                    response = self._whois_raw_query(domain, referral_server)
            
            # Parse response
            return self._parse_whois_response(response, domain)
            
        except Exception as e:
            return {'error': str(e), 'source': 'socket_direct'}
    
    def _whois_raw_query(self, domain, server, port=43):
        """Raw WHOIS socket query"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        sock.connect((server, port))
        sock.send(f"{domain}\r\n".encode())
        
        response = b""
        while True:
            try:
                data = sock.recv(4096)
                if not data:
                    break
                response += data
            except:
                break
        sock.close()
        
        return response.decode('utf-8', errors='ignore')
    
    def _whois_http_api(self, domain):
        """WHOIS lookup via HTTP APIs (bypasses many restrictions)"""
        apis = [
            f"https://api.domainsdb.info/v1/domains/search?domain={domain}",
            f"https://api.ip2whois.com/v1?key=free&domain={domain}",
        ]
        
        for api_url in apis:
            try:
                req = urllib.request.Request(api_url)
                req.add_header('User-Agent', 'Mozilla/5.0')
                with urllib.request.urlopen(req, timeout=5) as resp:
                    data = json.loads(resp.read().decode())
                    
                    info = {'source': 'http_api', 'api_url': api_url}
                    
                    if 'domains' in data and data['domains']:
                        domain_data = data['domains'][0]
                        if 'country' in domain_data: info['country'] = domain_data['country']
                        if 'isp' in domain_data: info['isp'] = domain_data['isp']
                        if 'organization' in domain_data: info['organization'] = domain_data['organization']
                        if 'create_date' in domain_data: info['creation_date'] = domain_data['create_date']
                        if 'expiration_date' in domain_data: info['expiration_date'] = domain_data['expiration_date']
                        if 'updated_date' in domain_data: info['updated_date'] = domain_data['updated_date']
                        
                    return info
            except:
                continue
        
        return None
    
    def _whois_rdap_lookup(self, domain):
        """RDAP lookup (modern WHOIS alternative, harder to block)"""
        try:
            tld = domain.split('.')[-1].lower()
            rdap_servers = {
                'com': 'https://rdap.verisign.com/com/v1/domain/',
                'net': 'https://rdap.verisign.com/net/v1/domain/',
                'org': 'https://rdap.pir.org/rdap/domain/',
            }
            
            base_url = rdap_servers.get(tld, f'https://rdap.verisign.com/{tld}/v1/domain/')
            url = base_url + domain
            
            req = urllib.request.Request(url)
            req.add_header('Accept', 'application/json')
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                
                info = {'source': 'rdap'}
                
                # Extract non-private information
                if 'events' in data:
                    for event in data['events']:
                        if event.get('eventAction') == 'registration':
                            info['creation_date'] = event.get('eventDate', '')
                        elif event.get('eventAction') == 'expiration':
                            info['expiration_date'] = event.get('eventDate', '')
                
                # Get entities (registrant, admin, tech)
                if 'entities' in data:
                    for entity in data['entities']:
                        roles = entity.get('roles', [])
                        if 'registrant' in roles:
                            vcard = entity.get('vcardArray', [])
                            if len(vcard) > 1:
                                info['registrant'] = self._parse_vcard(vcard[1])
                        elif 'administrative' in roles:
                            vcard = entity.get('vcardArray', [])
                            if len(vcard) > 1:
                                info['admin'] = self._parse_vcard(vcard[1])
                
                if 'nameservers' in data:
                    info['nameservers'] = [ns.get('ldhName', '') for ns in data['nameservers']]
                
                if 'status' in data:
                    info['status'] = data['status']
                
                return info
                
        except Exception as e:
            return None
    
    def _parse_vcard(self, vcard_data):
        """Parse vCard data from RDAP"""
        info = {}
        for item in vcard_data:
            if len(item) >= 4:
                prop_name = item[0]
                prop_value = item[3]
                if prop_name == 'fn':
                    info['name'] = prop_value
                elif prop_name == 'org':
                    info['organization'] = prop_value
                elif prop_name == 'email':
                    info['email'] = prop_value
                elif prop_name == 'tel':
                    info['phone'] = prop_value
                elif prop_name == 'adr':
                    if isinstance(prop_value, list) and len(prop_value) >= 3:
                        info['address'] = ', '.join([str(x) for x in prop_value if x])
        return info
    
    def _whois_history_check(self, domain):
        """Check WHOIS history and archived records (often bypasses current privacy)"""
        info = {'source': 'history_check'}
        
        # Check DNS history
        try:
            # Historical DNS can reveal original registrar
            url = f"https://securitytrails.com/api/v1/history/{domain}/whois"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            
            with urllib.request.urlopen(req, timeout=5) as resp:
                data = json.loads(resp.read().decode())
                if 'result' in data and data['result']:
                    # Get oldest record which often has original info
                    oldest = data['result'][-1] if data['result'] else {}
                    if 'registrar' in oldest:
                        info['historical_registrar'] = oldest['registrar']
                    return info
        except:
            pass
        
        return None
    
    def _whois_dns_trick(self, domain):
        """Extract info from DNS records (bypasses WHOIS privacy)"""
        info = {'source': 'dns_trick'}
        
        try:
            # SOA record often contains admin email
            import dns.resolver
            resolver = dns.resolver.Resolver()
            resolver.timeout = 3
            resolver.lifetime = 3
            
            try:
                answers = resolver.resolve(domain, 'SOA')
                for rdata in answers:
                    soa = str(rdata).split()
                    if len(soa) >= 2:
                        info['soa_mname'] = soa[0]  # Primary nameserver
                        info['soa_rname'] = soa[1]  # Admin email (replace first . with @)
            except:
                pass
            
            # TXT records
            try:
                answers = resolver.resolve(domain, 'TXT')
                for rdata in answers:
                    txt = str(rdata).strip('"')
                    if 'google-site-verification' in txt.lower():
                        info['has_google_verification'] = True
                    if 'v=spf1' in txt.lower():
                        info['has_spf'] = True
                        # SPF can reveal hosting info
                        if 'include:' in txt:
                            info['spf_includes'] = re.findall(r'include:([^\s]+)', txt)
                    if 'MS=' in txt:
                        info['has_microsoft_verification'] = True
            except:
                pass
            
            # MX records reveal email provider
            try:
                answers = resolver.resolve(domain, 'MX')
                mx_records = []
                for rdata in answers:
                    mx_records.append(str(rdata.exchange))
                if mx_records:
                    info['mx_records'] = mx_records
                    # Deduce email provider
                    for mx in mx_records:
                        if 'google' in mx or 'googlemail' in mx:
                            info['email_provider'] = 'Google Workspace'
                        elif 'outlook' in mx or 'protection.outlook' in mx:
                            info['email_provider'] = 'Microsoft 365'
                        elif 'zoho' in mx:
                            info['email_provider'] = 'Zoho Mail'
            except:
                pass
            
            return info
            
        except ImportError:
            # Fallback without dnspython
            try:
                # Use system nslookup
                result = subprocess.run(['nslookup', '-type=SOA', domain], 
                                      capture_output=True, text=True, timeout=3)
                if result.stdout:
                    info['soa_raw'] = result.stdout
            except:
                pass
            return info
    
    def _whois_hosting_leak(self, domain):
        """Extract owner info from hosting platform leaks"""
        info = {'source': 'hosting_leak'}
        
        try:
            ip = socket.gethostbyname(domain)
            
            # Check reverse DNS
            try:
                hostname = socket.gethostbyaddr(ip)[0]
                info['hostname'] = hostname
                
                # Hostname often leaks hosting account/username
                parts = hostname.split('.')
                if len(parts) > 1:
                    if any(x in hostname.lower() for x in ['hostgator', 'bluehost', 'hostinger']):
                        # First part might be account name
                        info['possible_account'] = parts[0]
            except:
                pass
            
            # Check SSL certificate (often contains real org name)
            try:
                ctx = ssl.create_default_context()
                with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                    s.settimeout(3)
                    s.connect((domain, 443))
                    cert = s.getpeercert()
                    
                    # Certificate organization often bypasses WHOIS privacy
                    subject = dict(x[0] for x in cert['subject'])
                    if 'organizationName' in subject:
                        info['cert_organization'] = subject['organizationName']
                    if 'commonName' in subject:
                        info['cert_common_name'] = subject['commonName']
                    
                    # Check Subject Alternative Names
                    if 'subjectAltName' in cert:
                        sans = [x[1] for x in cert['subjectAltName']]
                        info['cert_sans'] = sans[:10]
                        info['total_domains_on_cert'] = len(sans)
            except:
                pass
            
            # Check HTTP headers
            try:
                req = urllib.request.Request(f"https://{domain}")
                req.add_header('User-Agent', 'Mozilla/5.0')
                with urllib.request.urlopen(req, timeout=3) as resp:
                    headers = dict(resp.headers)
                    
                    # Headers that might leak info
                    leaky_headers = ['X-Powered-By', 'Server', 'X-Generator', 
                                   'X-Drupal-Cache', 'X-Drupal-Dynamic-Cache']
                    for header in leaky_headers:
                        if header in headers:
                            info[header.lower()] = headers[header]
            except:
                pass
            
            return info
            
        except Exception as e:
            return None
    
    def _parse_whois_response(self, response, domain):
        """Parse WHOIS response to extract information"""
        info = {
            'source': 'socket_direct',
            'raw_length': len(response),
            'has_privacy': False,
            'fields_found': 0
        }
        
        # Patterns for common WHOIS fields
        patterns = {
            'registrar': [
                r'(?:Registrar|Sponsoring Registrar):\s*(.+)',
                r'Registrar Name:\s*(.+)',
            ],
            'creation_date': [
                r'(?:Creation Date|Created On|Registration Time|Domain Registration Date):\s*(.+)',
                r'Registered on:\s*(.+)',
            ],
            'expiration_date': [
                r'(?:Registrar Registration Expiration Date|Expiry Date|Registry Expiry Date|Expiration Date):\s*(.+)',
                r'Expiry date:\s*(.+)',
            ],
            'updated_date': [
                r'(?:Updated Date|Last Updated On|Last Modified):\s*(.+)',
                r'Last updated:\s*(.+)',
            ],
            'name_servers': [
                r'Name Server:\s*(.+)',
                r'nserver:\s*(.+)',
            ],
            'registrant_name': [
                r'Registrant Name:\s*(.+)',
                r'Registrant:\s*(.+)',
            ],
            'registrant_org': [
                r'Registrant Organization:\s*(.+)',
                r'Registrant Org:\s*(.+)',
            ],
            'registrant_email': [
                r'Registrant Email:\s*(.+)',
                r'Registrant E-mail:\s*(.+)',
            ],
            'registrant_phone': [
                r'Registrant Phone:\s*(.+)',
            ],
            'admin_email': [
                r'Admin Email:\s*(.+)',
            ],
            'tech_email': [
                r'Tech Email:\s*(.+)',
            ],
            'status': [
                r'(?:Domain Status|Status):\s*(.+)',
                r'Status:\s*(.+)',
            ],
            'dnssec': [
                r'DNSSEC:\s*(.+)',
            ]
        }
        
        # Check for privacy protection indicators
        privacy_indicators = [
            'redacted for privacy', 'privacy protect', 'whois guard',
            'private registration', 'contact privacy', 'domains by proxy',
            'whoisproxy', 'privacy service', 'registration private',
            'perfect privacy', 'whois privacy', 'private whois'
        ]
        
        for indicator in privacy_indicators:
            if indicator.lower() in response.lower():
                info['has_privacy'] = True
                info['privacy_type'] = indicator
                break
        
        # Extract fields
        for field, field_patterns in patterns.items():
            for pattern in field_patterns:
                matches = re.findall(pattern, response, re.IGNORECASE | re.MULTILINE)
                if matches:
                    if field == 'name_servers':
                        info[field] = [ns.strip().lower() for ns in matches]
                    else:
                        info[field] = matches[0].strip()
                    info['fields_found'] += 1
                    break
        
        # Extract email addresses (even from privacy-protected records)
        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', response)
        if emails:
            # Filter out common privacy emails
            real_emails = [e for e in emails if not any(p in e.lower() for p in 
                         ['privacy', 'proxy', 'whois', 'private', 'contact', 'abuse', 'noreply'])]
            if real_emails:
                info['emails_found'] = list(set(real_emails))
        
        return info
    
    def start_scan(self):
        """Fast scan"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Enter URL")
            return
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        self.scan_btn.config(state='disabled', text="⏳ SCANNING...")
        self.deep_btn.config(state='disabled')
        self.progress_var.set(0)
        self.status_var.set("⚡ Fast Scanning...")
        
        thread = threading.Thread(target=self.run_scan, args=(url, False))
        thread.daemon = True
        thread.start()
    
    def start_deep_scan(self):
        """Deep scan with WHOIS bypass"""
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Enter URL")
            return
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        self.scan_btn.config(state='disabled')
        self.deep_btn.config(state='disabled', text="⏳ DEEP SCANNING...")
        self.progress_var.set(0)
        self.status_var.set("🔍 Deep Scanning with WHOIS Privacy Bypass...")
        
        thread = threading.Thread(target=self.run_scan, args=(url, True))
        thread.daemon = True
        thread.start()
    
    def run_scan(self, url, deep_scan=False):
        """Execute scan"""
        start_time = time.time()
        
        try:
            domain, ip = self.get_domain_ip(url)
            self.root.after(0, lambda: self.progress_var.set(10))
            
            # Parallel data collection
            with ThreadPoolExecutor(max_workers=8) as executor:
                future_geo = executor.submit(self.get_geo_fast, ip)
                future_ssl = executor.submit(self.get_ssl_fast, domain)
                future_headers = executor.submit(self.get_headers_fast, url)
                future_ports = executor.submit(self.scan_ports_fast, ip)
                future_dns = executor.submit(self.get_dns_info, domain)
                
                if deep_scan:
                    future_whois = executor.submit(self.whois_query, domain)
                
                geo = future_geo.result()
                ssl_info = future_ssl.result()
                headers = future_headers.result()
                open_ports = future_ports.result()
                dns_info = future_dns.result()
                
                if deep_scan:
                    whois_results = future_whois.result()
            
            self.root.after(0, lambda: self.progress_var.set(60))
            
            hosting = self.detect_hosting_fast(domain, ip, headers)
            tech = self.detect_tech_fast(url)
            
            self.root.after(0, lambda: self.progress_var.set(80))
            
            # Update tabs
            self.root.after(0, lambda: self.update_hosting_tab(
                domain, ip, hosting, geo, ssl_info, open_ports))
            
            self.root.after(0, lambda: self.update_dns_tab(domain, dns_info))
            
            self.root.after(0, lambda: self.update_headers_tab(headers))
            
            self.root.after(0, lambda: self.update_tech_tab(tech))
            
            self.root.after(0, lambda: self.update_security_tab(headers, domain, ssl_info))
            
            if deep_scan:
                self.root.after(0, lambda: self.update_whois_tab_deep(whois_results, domain))
            else:
                self.root.after(0, lambda: self.update_whois_tab_basic(domain))
            
            self.root.after(0, lambda: self.progress_var.set(100))
            
            if deep_scan:
                self.root.after(0, lambda: self.notebook.select(5))  # WHOIS tab
            
            scan_time = round(time.time() - start_time, 2)
            self.root.after(0, lambda: self.status_var.set(
                f"✅ {'Deep' if deep_scan else 'Fast'} Scan Complete in {scan_time}s | Hosting: {hosting}"))
            
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"❌ Error: {str(e)[:50]}"))
            
        finally:
            self.root.after(0, lambda: self.scan_btn.config(state='normal', text="⚡ FAST SCAN"))
            self.root.after(0, lambda: self.deep_btn.config(state='normal', text="🔍 DEEP SCAN (WHOIS BYPASS)"))
    
    def get_domain_ip(self, url):
        """Get domain and IP"""
        domain = re.sub(r'^https?://', '', url)
        domain = re.sub(r'^www\.', '', domain)
        domain = domain.split('/')[0].split(':')[0]
        
        try:
            ip = socket.gethostbyname(domain)
        except:
            ip = "Unknown"
        
        return domain, ip
    
    def get_geo_fast(self, ip):
        """Fast geolocation"""
        if ip in self.scan_cache:
            return self.scan_cache[ip]
        
        try:
            url = f"http://ip-api.com/json/{ip}?fields=status,country,countryCode,regionName,city,zip,lat,lon,timezone,isp,org,as,query"
            req = urllib.request.Request(url)
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=2) as resp:
                geo = json.loads(resp.read().decode())
                self.scan_cache[ip] = geo
                return geo
        except:
            return None
    
    def scan_ports_fast(self, ip, ports=[80, 443, 21, 22, 25, 3306, 8080]):
        """Fast port scan"""
        open_ports = []
        
        def check_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    return port
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=len(ports)) as executor:
            futures = {executor.submit(check_port, port): port for port in ports}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    service_map = {80: 'HTTP', 443: 'HTTPS', 21: 'FTP', 22: 'SSH', 
                                 25: 'SMTP', 3306: 'MySQL', 8080: 'HTTP-Alt'}
                    open_ports.append((result, service_map.get(result, 'Unknown')))
        
        return open_ports
    
    def get_ssl_fast(self, domain):
        """Fast SSL check"""
        try:
            ctx = ssl.create_default_context()
            with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
                s.settimeout(2)
                s.connect((domain, 443))
                cert = s.getpeercert()
                
                not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                days_left = (not_after - datetime.now()).days
                
                return {
                    'issuer': dict(x[0] for x in cert['issuer']),
                    'days_left': days_left,
                    'notBefore': cert['notBefore'],
                    'notAfter': cert['notAfter'],
                    'subject': dict(x[0] for x in cert['subject']) if cert.get('subject') else {}
                }
        except:
            return None
    
    def get_headers_fast(self, url):
        """Fast headers"""
        try:
            req = urllib.request.Request(url, method='HEAD')
            req.add_header('User-Agent', 'Mozilla/5.0')
            with urllib.request.urlopen(req, timeout=3) as resp:
                headers = dict(resp.headers)
                headers['_status'] = resp.status
                return headers
        except:
            return None
    
    def get_dns_info(self, domain):
        """Get DNS information"""
        info = {}
        
        try:
            # A record
            info['a_record'] = socket.gethostbyname(domain)
        except:
            pass
        
        try:
            # AAAA record
            addr_info = socket.getaddrinfo(domain, None, socket.AF_INET6)
            info['aaaa_records'] = list(set([a[4][0] for a in addr_info]))
        except:
            pass
        
        try:
            # CNAME and reverse
            hostname, aliases, ips = socket.gethostbyname_ex(domain)
            if aliases:
                info['cname'] = aliases
            if ips:
                try:
                    info['reverse_dns'] = socket.gethostbyaddr(ips[0])[0]
                except:
                    pass
        except:
            pass
        
        return info
    
    def detect_hosting_fast(self, domain, ip, headers):
        """Detect hosting"""
        try:
            try:
                hostname = socket.gethostbyaddr(ip)[0].lower()
            except:
                hostname = ''
            
            for pattern, provider in self.hosting_providers.items():
                if pattern in hostname:
                    return provider
            
            if headers:
                server = headers.get('Server', '').lower()
                for pattern, provider in self.hosting_providers.items():
                    if pattern in server:
                        return provider
            
            geo = self.get_geo_fast(ip)
            if geo and geo.get('org'):
                org = geo['org'].lower()
                for pattern, provider in self.hosting_providers.items():
                    if pattern in org:
                        return provider
        except:
            pass
        
        return "Unknown / Possibly Shared Hosting"
    
    def detect_tech_fast(self, url):
        """Detect technologies"""
        tech = []
        headers = self.get_headers_fast(url)
        
        if headers:
            server = headers.get('Server', '').lower()
            if 'apache' in server: tech.append('Apache')
            elif 'nginx' in server: tech.append('Nginx')
            elif 'iis' in server: tech.append('IIS')
            elif 'cloudflare' in server: tech.append('Cloudflare')
            
            powered = headers.get('X-Powered-By', '').lower()
            if 'php' in powered: tech.append('PHP')
            elif 'asp.net' in powered: tech.append('ASP.NET')
            
            if 'cf-ray' in headers: tech.append('Cloudflare')
        
        return tech
    
    def update_hosting_tab(self, domain, ip, hosting, geo, ssl_info, open_ports):
        """Update hosting tab"""
        text = self.tabs['hosting']
        text.delete(1.0, tk.END)
        
        lines = []
        lines.append(("╔══════════════════════════════════════════════════╗\n", 'header'))
        lines.append(("║        🏢 HOSTING & IP INTELLIGENCE              ║\n", 'header'))
        lines.append(("╚══════════════════════════════════════════════════╝\n\n", 'header'))
        
        lines.append(("📌 HOSTING PROVIDER:\n", 'subheader'))
        lines.append((f"   Provider: {hosting}\n\n", 'highlight'))
        
        lines.append(("📌 IP ADDRESS:\n", 'subheader'))
        lines.append((f"   IP: {ip}\n", 'info'))
        lines.append((f"   Domain: {domain}\n\n", 'info'))
        
        if geo and geo.get('status') == 'success':
            lines.append(("📍 LOCATION:\n", 'subheader'))
            lines.append((f"   Country: {geo.get('country', 'N/A')} ({geo.get('countryCode', 'N/A')})\n", 'info'))
            lines.append((f"   City: {geo.get('city', 'N/A')}, {geo.get('regionName', 'N/A')}\n", 'info'))
            lines.append((f"   ISP: {geo.get('isp', 'N/A')}\n", 'info'))
            lines.append((f"   Organization: {geo.get('org', 'N/A')}\n", 'info'))
            lines.append((f"   ASN: {geo.get('as', 'N/A')}\n", 'info'))
            lines.append((f"   Timezone: {geo.get('timezone', 'N/A')}\n\n", 'info'))
        
        if ssl_info:
            lines.append(("🔒 SSL CERTIFICATE:\n", 'subheader'))
            lines.append((f"   Issuer: {ssl_info['issuer'].get('organizationName', 'Unknown')}\n", 'info'))
            days = ssl_info['days_left']
            status = 'VALID ✓' if days > 30 else 'EXPIRING ⚠'
            color = 'success' if days > 30 else 'warning'
            lines.append((f"   Status: {status} ({days} days)\n\n", color))
            
            # Show cert organization (may bypass WHOIS privacy)
            subject = ssl_info.get('subject', {})
            if 'organizationName' in subject:
                lines.append((f"   Cert Organization: {subject['organizationName']}\n", 'bypass'))
            if 'commonName' in subject:
                lines.append((f"   Common Name: {subject['commonName']}\n\n", 'info'))
        
        if open_ports:
            lines.append(("🔌 OPEN PORTS:\n", 'subheader'))
            for port, service in open_ports:
                lines.append((f"   ✓ Port {port} ({service})\n", 'success'))
        
        for line, tag in lines:
            text.insert(tk.END, line, tag)
    
    def update_dns_tab(self, domain, dns_info):
        """Update DNS tab"""
        text = self.tabs['dns']
        text.delete(1.0, tk.END)
        
        lines = [
            ("╔══════════════════════════════════════════════════╗\n", 'header'),
            ("║             📡 DNS RECORDS                        ║\n", 'header'),
            ("╚══════════════════════════════════════════════════╝\n\n", 'header'),
        ]
        
        if 'a_record' in dns_info:
            lines.append(("📌 A RECORD (IPv4):\n", 'subheader'))
            lines.append((f"   {domain} → {dns_info['a_record']}\n\n", 'success'))
        
        if 'aaaa_records' in dns_info:
            lines.append(("📌 AAAA RECORD (IPv6):\n", 'subheader'))
            for addr in dns_info['aaaa_records']:
                lines.append((f"   {domain} → {addr}\n", 'success'))
            lines.append(("\n", None))
        
        if 'cname' in dns_info:
            lines.append(("📌 CNAME:\n", 'subheader'))
            for alias in dns_info['cname']:
                lines.append((f"   {alias}\n", 'info'))
            lines.append(("\n", None))
        
        if 'reverse_dns' in dns_info:
            lines.append(("📌 PTR (Reverse DNS):\n", 'subheader'))
            lines.append((f"   {dns_info['a_record']} → {dns_info['reverse_dns']}\n\n", 'info'))
        
        for line, tag in lines:
            text.insert(tk.END, line, tag)
    
    def update_headers_tab(self, headers):
        """Update headers tab"""
        text = self.tabs['headers']
        text.delete(1.0, tk.END)
        
        lines = [
            ("╔══════════════════════════════════════════════════╗\n", 'header'),
            ("║           📨 HTTP RESPONSE HEADERS                ║\n", 'header'),
            ("╚══════════════════════════════════════════════════╝\n\n", 'header'),
        ]
        
        if headers:
            status = headers.get('_status', 'Unknown')
            lines.append((f"📊 Status Code: {status}\n\n", 'success' if status == 200 else 'warning'))
            
            important = ['Server', 'Content-Type', 'X-Powered-By', 'Set-Cookie']
            for key in important:
                if key in headers:
                    lines.append((f"   {key}: {headers[key]}\n", 'info'))
            
            lines.append(("\n📋 All Headers:\n", 'subheader'))
            for key, value in sorted(headers.items()):
                if key != '_status' and key not in important:
                    val = str(value)[:80]
                    lines.append((f"   {key}: {val}\n", 'info'))
        else:
            lines.append(("   Failed to retrieve headers\n", 'error'))
        
        for line, tag in lines:
            text.insert(tk.END, line, tag)
    
    def update_tech_tab(self, tech):
        """Update technology tab"""
        text = self.tabs['tech']
        text.delete(1.0, tk.END)
        
        lines = [
            ("╔══════════════════════════════════════════════════╗\n", 'header'),
            ("║           ⚙️ TECHNOLOGIES DETECTED                ║\n", 'header'),
            ("╚══════════════════════════════════════════════════╝\n\n", 'header'),
        ]
        
        if tech:
            lines.append((f"📦 Found {len(tech)} technologies:\n\n", 'subheader'))
            for t in tech:
                lines.append((f"   ✓ {t}\n", 'success'))
        else:
            lines.append(("   No technologies detected\n", 'warning'))
        
        for line, tag in lines:
            text.insert(tk.END, line, tag)
    
    def update_security_tab(self, headers, domain, ssl_info):
        """Update security tab"""
        text = self.tabs['security']
        text.delete(1.0, tk.END)
        
        lines = [
            ("╔══════════════════════════════════════════════════╗\n", 'header'),
            ("║           🔒 SECURITY ANALYSIS                    ║\n", 'header'),
            ("╚══════════════════════════════════════════════════╝\n\n", 'header'),
        ]
        
        if headers:
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'CSP',
                'X-Frame-Options': 'Clickjacking Protection',
                'X-Content-Type-Options': 'MIME Protection',
                'X-XSS-Protection': 'XSS Protection'
            }
            
            score = 0
            lines.append(("🛡️ SECURITY HEADERS:\n", 'subheader'))
            for header, desc in security_headers.items():
                if header in headers:
                    lines.append((f"   ✓ {header}: Present\n", 'success'))
                    score += 1
                else:
                    lines.append((f"   ✗ {header}: Missing\n", 'error'))
            
            lines.append((f"\n📊 Score: {score}/{len(security_headers)}\n\n", 
                         'success' if score >= 4 else 'warning'))
        
        if ssl_info:
            lines.append(("🔐 SSL/TLS:\n", 'subheader'))
            lines.append((f"   Status: {'VALID' if ssl_info['days_left'] > 0 else 'EXPIRED'}\n", 
                         'success' if ssl_info['days_left'] > 0 else 'error'))
            lines.append((f"   Expires: {ssl_info['notAfter']}\n", 'info'))
        
        for line, tag in lines:
            text.insert(tk.END, line, tag)
    
    def update_whois_tab_basic(self, domain):
        """Basic WHOIS tab"""
        text = self.tabs['whois']
        text.delete(1.0, tk.END)
        
        lines = [
            ("╔══════════════════════════════════════════════════╗\n", 'header'),
            ("║           📋 WHOIS INFORMATION (BASIC)            ║\n", 'header'),
            ("╚══════════════════════════════════════════════════╝\n\n", 'header'),
            (f"   Domain: {domain}\n\n", 'info'),
            ("   ℹ️ Basic scan shows limited WHOIS data\n\n", 'warning'),
            ("   🔍 Click 'DEEP SCAN (WHOIS BYPASS)' for:\n", 'subheader'),
            ("   • Privacy protection bypass\n", 'bypass'),
            ("   • Historical WHOIS records\n", 'bypass'),
            ("   • DNS-based owner detection\n", 'bypass'),
            ("   • SSL certificate owner info\n", 'bypass'),
            ("   • Hosting account leaks\n", 'bypass'),
            ("   • Email provider detection\n", 'bypass'),
            ("   • Multiple WHOIS source aggregation\n\n", 'bypass'),
            ("   📊 Deep scan uses 6 different bypass methods\n", 'info'),
        ]
        
        for line, tag in lines:
            text.insert(tk.END, line, tag)
    
    def update_whois_tab_deep(self, whois_results, domain):
        """Deep WHOIS tab with all bypass results"""
        text = self.tabs['whois']
        text.delete(1.0, tk.END)
        
        lines = []
        lines.append(("╔══════════════════════════════════════════════════╗\n", 'header'))
        lines.append(("║      📋 WHOIS DEEP SCAN (PRIVACY BYPASS)         ║\n", 'header'))
        lines.append(("╚══════════════════════════════════════════════════╝\n\n", 'header'))
        
        lines.append((f"   🎯 Target Domain: {domain}\n", 'highlight'))
        lines.append((f"   📊 Bypass Methods Used: {len(whois_results)}\n\n", 'info'))
        
        # Check if privacy was detected and bypassed
        privacy_bypassed = False
        total_info_found = 0
        
        for method_name, result in whois_results.items():
            if not result:
                continue
            
            method_display = method_name.replace('_whois_', '').replace('_', ' ').title()
            
            if isinstance(result, dict):
                if 'has_privacy' in result and result['has_privacy']:
                    privacy_bypassed = True
                    lines.append((f"🔓 PRIVACY DETECTED & BYPASSED!\n", 'bypass'))
                    lines.append((f"   Type: {result.get('privacy_type', 'Unknown')}\n", 'warning'))
                
                # Extract all useful information
                useful_fields = [
                    'registrar', 'creation_date', 'expiration_date', 'updated_date',
                    'registrant_name', 'registrant_org', 'registrant_email', 'registrant_phone',
                    'admin_email', 'tech_email', 'emails_found', 'name_servers',
                    'status', 'dnssec', 'country', 'isp', 'organization',
                    'cert_organization', 'cert_common_name', 'email_provider',
                    'possible_account', 'soa_rname', 'soa_mname',
                    'historical_registrar', 'total_domains_on_cert'
                ]
                
                method_info_found = 0
                for field in useful_fields:
                    if field in result and result[field]:
                        method_info_found += 1
                        field_name = field.replace('_', ' ').title()
                        value = result[field]
                        
                        if isinstance(value, list):
                            value = ', '.join(str(v) for v in value[:5])
                            if len(result[field]) > 5:
                                value += f" ... (+{len(result[field])-5} more)"
                        
                        if len(str(value)) > 80:
                            value = str(value)[:77] + "..."
                        
                        # Use bypass tag for fields that indicate successful bypass
                        tag = 'bypass' if any(x in field for x in ['registrant', 'email', 'organization', 'cert_']) else 'info'
                        lines.append((f"   • {field_name}: {value}\n", tag))
                
                if method_info_found > 0:
                    total_info_found += method_info_found
        
        # Summary
        lines.append(("\n" + "=" * 50 + "\n", 'info'))
        lines.append(("📊 BYPASS SUMMARY:\n", 'subheader'))
        
        if privacy_bypassed:
            lines.append((f"   ✅ Privacy Protection: BYPASSED\n", 'success'))
        else:
            lines.append((f"   ℹ️ No privacy protection detected\n", 'info'))
        
        lines.append((f"   📈 Total Information Points Found: {total_info_found}\n", 
                     'success' if total_info_found > 10 else 'warning'))
        lines.append((f"   🔍 Bypass Methods Executed: {len(whois_results)}\n\n", 'info'))
        
        lines.append(("💡 BYPASS TECHNIQUES USED:\n", 'subheader'))
        lines.append(("   1. Direct WHOIS Socket Query\n", 'info'))
        lines.append(("   2. HTTP WHOIS API (Multiple Providers)\n", 'info'))
        lines.append(("   3. RDAP Lookup (Modern Protocol)\n", 'info'))
        lines.append(("   4. Historical WHOIS Records\n", 'info'))
        lines.append(("   5. DNS Record Analysis (SOA/MX/TXT)\n", 'info'))
        lines.append(("   6. SSL Certificate Information Leak\n", 'info'))
        lines.append(("   7. Hosting Platform Information Leak\n", 'info'))
        lines.append(("   8. Reverse DNS & IP Intelligence\n", 'info'))
        
        for line, tag in lines:
            text.insert(tk.END, line, tag)
    
    def clear_results(self):
        """Clear all tabs"""
        for text_widget in self.tabs.values():
            text_widget.delete(1.0, tk.END)
        self.progress_var.set(0)
        self.status_var.set("● Ready - Fast Scan or Deep Scan with WHOIS Bypass")
        self.scan_cache = {}
    
    def open_browser(self):
        """Open URL"""
        url = self.url_entry.get().strip()
        if url:
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            webbrowser.open(url)
    
    def export_report(self):
        """Export report"""
        try:
            url = self.url_entry.get().strip()
            domain = re.sub(r'^https?://', '', url).split('/')[0]
            filename = f"scan_report_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("=" * 60 + "\n")
                f.write("ULTRA FAST WEBSITE INFO HUNTER PRO - SCAN REPORT\n")
                f.write("=" * 60 + "\n")
                f.write(f"Target: {url}\n")
                f.write(f"Date: {datetime.now()}\n")
                f.write(f"Developer: CHOWDHURY-VAI\n")
                f.write(f"Facebook: https://facebook.com/itbossusa\n")
                f.write("=" * 60 + "\n\n")
                
                for tab_id in ['hosting', 'dns', 'headers', 'tech', 'security', 'whois']:
                    content = self.tabs[tab_id].get(1.0, tk.END).strip()
                    if content:
                        f.write(content + "\n\n")
            
            messagebox.showinfo("✅ Success", f"Report saved: {filename}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def main():
    root = tk.Tk()
    app = UltraFastWebsiteHunter(root)
    root.mainloop()

if __name__ == "__main__":
    main()