from utils.encounter import Encounter, Roll, Item, Member


class Test_Encounter_Unit:

    test_data = [['7/13/2021 18:07', 'AddLoot', '', 'Byakko Totem', 0, 1],['7/13/2021 18:07', 'GreedLoot', 'Your Character', 'Byakko Totem', 34, 1],['7/13/2021 18:07', 'ObtainLoot', 'Your Character', 'Byakko Totem', 0, 1]]
    test_encounter = Encounter(test_data)
    row = ['7/13/2021 18:07', 'GreedLoot', 'Test Character', 'Byakko Sword', 12, 1]

    member = Member(test_data[1][2])
    item = Item(test_data[0][3], test_data[0][5], 0)

    expected_loot = {item}
    expected_members = {member.name: member}
    expected_time = test_data[0][0]
    expected_rolls = {Roll(test_data[1][1],member, test_data[1][4],item)}

    new_loot = Item(row[3],row[5],99)
    new_member = Member(row[2])
    new_roll = Roll(row[1],new_member,row[4],new_loot)

    def test_Encounter_instantiate(self):
        assert isinstance(self.test_encounter, Encounter)
    def test_Encounter_init_rows(self):
        assert self.test_encounter.rows == self.test_data
    def test_Encounter_init_time(self):
        assert self.test_encounter.cleartime == self.expected_time
    def test_Encounter_init_members(self):
        assert self.test_encounter.members == self.expected_members
    def test_Encounter_init_loot(self):
        assert self.test_encounter.loot == self.expected_loot
    def test_Encounter_init_rolls(self):
        assert self.test_encounter.rolls == self.expected_rolls
    def test_Encounter_add_row(self):
        assert self.test_encounter.add_row(self.row) == self.test_data.append(self.row)
        assert self.test_encounter.rows[-1] == self.row
    def test_Encounter_get_members(self):
        assert self.test_encounter.get_members() == self.expected_members
    def test_Encounter_add_member(self):
        assert self.test_encounter.add_member(Member) == self.expected_members.add(self.new_member)
        assert self.new_member in self.test_encounter.members
    def test_Encounter_get_loot(self):
        assert self.test_encounter.get_loot() == self.expected_loot
    def test_Encounter_add_loot(self):
        assert self.test_encounter.add_loot(Item) == self.expected_loot.add(self.new_loot)
        assert self.new_loot in self.test_encounter.loot
    def test_Encounter_get_rolls(self):
        assert self.test_encounter.get_rolls() == self.expected_rolls
    def test_Encounter_add_roll(self):
        assert self.test_encounter.add_roll(Roll) == self.expected_rolls.add(self.new_roll)
        assert self.new_roll in self.test_encounter.rolls
    