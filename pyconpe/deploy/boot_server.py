# Exemplo de como bootar usando o boto
from boto.ec2.connection import EC2Connection

centos_ami = 'ami-9110c7f8'

conn = EC2Connection(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY)
image = conn.get_all_images(image_ids=[centos_ami])[0]
reservation = image.run(
        key_name='trouver', security_groups=['default'],
        instance_type='t1.micro',
    )

instance = reservation.instances[0]
print instance.state
print instance.update()
print instance.public_dns_name
