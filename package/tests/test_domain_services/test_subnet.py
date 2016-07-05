from unittest import TestCase

from mock import Mock

from cloudshell.cp.aws.domain.services.ec2.subnet import SubnetService


class TestSubnetService(TestCase):
    def setUp(self):

        self.vpc = Mock()
        self.cidr = '10.0.0.0/24'
        self.vpc_name = 'name'
        self.reservation_id = 'res'
        self.tag_srv = Mock()
        self.subnet_waiter = Mock()
        self.subnet_srv = SubnetService(self.tag_srv, self.subnet_waiter)

    def test_create_subnet_for_vpc(self):
        subnet = self.subnet_srv.create_subnet_for_vpc(self.vpc, self.cidr, self.vpc_name, self.reservation_id)
        self.assertTrue(self.vpc.create_subnet.called_with(self.cidr))
        self.assertTrue(self.subnet_waiter.wait.called_with(subnet, 'available'))
        self.assertTrue(self.tag_srv.get_default_tags.called_with(self.vpc_name, self.reservation_id))
        self.assertEqual(subnet, self.vpc.create_subnet())

    def test_get_subnet_from_vpc(self):
        vpc = Mock()
        vpc.subnets = Mock()
        vpc.subnets.all = Mock(return_value=[1])
        subnet = self.subnet_srv.get_subnet_from_vpc(vpc)
        self.assertEqual(1, subnet)

    def test_get_subnet_from_vpc_fault(self):
        vpc = Mock()
        vpc.subnets = Mock()
        vpc.subnets.all = Mock(return_value=[])
        self.assertRaises(ValueError, self.subnet_srv.get_subnet_from_vpc, vpc)

    def test_delete_subnet(self):
        subnet = Mock()
        res = self.subnet_srv.detele_subnet(subnet)
        self.assertTrue(res)
        self.assertTrue(subnet.delete.called)