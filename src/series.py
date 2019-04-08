import copy

class Series:
    name = ""
    brackets = []
    full_head_to_head = {}

    def __init__(self, name, brackets):
        self.name = name
        self.brackets = brackets
        self.full_head_to_head = self.combine_h2h(brackets)

    def __str__(self):
        return "%s: %s" % (self.name, self.brackets)

    def __repr__(self):
        return self.__str__()

    def combine_h2h(self, brackets):
        full_h2h = {}
        for bracket in brackets:
            full_h2h = self.merge_h2h(full_h2h, bracket.head_to_head)

        return full_h2h

    def merge_h2h(self, dict1, dict2):
        # https://stackoverflow.com/questions/55531786/how-to-merge-a-dictionary-with-two-lists-as-the-value
        result_dict = copy.deepcopy(
            dict1)  # to ensure result_dict is an entirely new object, and mutations on result_dict do not affect dict1

        for k, v in dict2.items():
            if k not in result_dict:
                result_dict[k] = v
            else:
                result_dict[k] = tuple(self.ordered_list_merge(lst1, lst2)
                                       for lst1, lst2 in
                                       zip(result_dict[k], v))

        return result_dict

    @staticmethod
    def ordered_list_merge(lst1, lst2):
        # https://stackoverflow.com/questions/55531786/how-to-merge-a-dictionary-with-two-lists-as-the-value


        resulting_list = lst1.copy()  # to ensure list 1 is not mutated by changes to resulting_list
        resulting_list.extend(x for x in lst2 if x not in resulting_list)
        return resulting_list

