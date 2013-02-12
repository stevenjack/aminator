#!/usr/bin/env python2.7
"""
"""
import logging
import botocore.session

from aminator import NullHandler

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(NullHandler())

_session = botocore.session.Session()
_ec2_data = {operation['name']: operation for operation in _session.get_service_data('ec2')['operations']}


def _find_state_enum(dictionary, path="", search_key='State'):
    ret = None
    if isinstance(dictionary, dict):
        if search_key in dictionary:
            if search_key == 'enum':
                log.debug(path, str(dictionary[search_key]))
                return dictionary[search_key]
            else:
                return _find_state_enum(dictionary[search_key], "%s['%s']" % (path, search_key), 'enum')
        else:
            for key in dictionary:
                ret = _find_state_enum(dictionary[key], "%s['%s']" % (path, key), search_key)
                if ret is not None:
                    break
            return ret


def ec2_op_states(op):
    return _find_state_enum(_ec2_data[op])


ec2_obj_states = {'Image': ec2_op_states('DescribeImages'),
                  'Volume': ec2_op_states('DescribeVolumes'),
                  'Snapshot': ec2_op_states('DescribeSnapshots'),
                  'Instance': ec2_op_states('DescribeInstances')}

ec2_obj_states['Image'].append('pending')
ec2_obj_states['Snapshot'].append('100%')


if __name__ == '__main__':
    for obj in ec2_obj_states:
        print '%s: %s' % (obj, ' | '.join(ec2_obj_states[obj]))