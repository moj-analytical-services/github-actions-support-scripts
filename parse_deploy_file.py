import os
import json

lookup = {
    '102PF Wifi': os.environ.get('IPS_102PF_WIFI'),
    'Digital Wifi and VPN': os.environ.get('IPS_DIGITAL'),
    'DOM1': os.environ.get('IPS_DOM1'),
    'QUANTUM': os.environ.get('IPS_QUANTUM'),
    'Alan Turing Institute': os.environ.get('IPS_TURING'),
    'MoJo': os.environ.get('IPS_MOJO'),
    'Any': ''
}

# with open('webapp-source/deploy.json') as input:
with open('../deploy.json') as input:
    print('Parsing deploy.json')
    data = json.load(input)

allowed = data.get('allowed_ip_ranges', [])
if 'Any' in allowed:
    ip_ranges = ['']
else:
    ip_ranges = [lookup[name] for name in allowed if name in lookup]
if not ip_ranges:
    ip_ranges = [lookup['DOM1']]

auth_required = not data.get('disable_authentication', False)
webapp_port = data.get('port', 80)

health_check = data.get('health_check', '/?healthz')

# The following are input values of the webapp helm chart
with open('deploy-params/overrides.yaml', 'w') as output:
    json.dump({
        'AuthProxy': {
            'AuthenticationRequired': auth_required,
            'IPRanges': ','.join(ip_ranges),
        },
        'WebApp': {
            'Port': webapp_port,
            'HealthCheck': health_check,
        }
    }, output)
print('Wrote deploy-params/overrides.yaml')
