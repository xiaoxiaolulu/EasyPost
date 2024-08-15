import collections


def get_tree_max_id(trees: list):
    """
    广度优先遍历树, 得到最大Tree max id
    """
    queue = collections.deque()
    queue.append(trees)
    max_id = 0
    while len(queue) != 0:
        sub_tree: list = queue.popleft()
        for node in sub_tree:
            children: list = node.get('children')
            max_id = max(max_id, node['id'])

            try:
                if len(children) > 0:
                    queue.append(children)
            except TypeError:
                continue
    return max_id


def get_relation_tree(value, relation_id):
    """
    根据目录id检索出当前层级以及下级的目录结构
    """
    tree = None
    if not value:
        return tree

    if isinstance(value, list):
        for content in value:  # content -> dict
            if int(content['id']) == int(relation_id):
                tree = content
            children = content.get('children')
            if children:
                get_relation_tree(children, relation_id)
    return tree


def collections_directory_id(value, relation_id):
    """
    根据目录id以列表的形式检索出当前目录以及下级目录的id
    """
    ids = [relation_id]
    if not value:
        return ids

    if isinstance(value, dict):
        ids.append(value.get('id'))
        for content in value["children"]:  # content -> dict
            if int(content['id']) == int(relation_id) or int(content['parent']) == int(relation_id):
                ids.append(content['id'])
            children = content.get('children')
            if children:
                collections_directory_id(children, relation_id)
    return ids


def use_role(value, role_id):
    trees = []
    if not value:
        return trees

    if isinstance(value, list):
        for content in value:  # content -> dict
            try:
                if int(role_id) in list(content['role']):
                    trees.append(content)
                children = content.get('subs')
                if children:
                    use_role(children, role_id)
            except KeyError:
                continue
    return trees
