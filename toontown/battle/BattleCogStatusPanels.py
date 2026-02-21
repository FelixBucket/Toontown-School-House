from direct.gui.DirectGui import *
from panda3d.core import *

PANEL_W = 0.22
PANEL_H = 0.20
PANEL_SPACING = 0.48
PANEL_COLOR = Vec4(0.65, 0.65, 0.65, 1)

DEPT_ICONS = {
    'c': 'CorpIcon',
    's': 'SalesIcon',
    'l': 'LegalIcon',
    'm': 'MoneyIcon',
}

DEPT_ICON_COLORS = {
    'c': Vec4(0.863, 0.776, 0.769, 1.0),
    's': Vec4(0.843, 0.745, 0.745, 1.0),
    'l': Vec4(0.749, 0.776, 0.824, 1.0),
    'm': Vec4(0.749, 0.769, 0.749, 1.0),
}


class BattleCogStatusPanels:

    def __init__(self, suits):
        self.suits = suits
        self.panels = []
        gui = loader.loadModel('phase_3.5/models/gui/battle_gui')
        cogIcons = loader.loadModel('phase_3/models/gui/cog_icons')
        numSuits = len(self.suits)
        startX = -PANEL_SPACING * (numSuits - 1) / 2.0
        for i, suit in enumerate(reversed(self.suits)):
            x = startX + i * PANEL_SPACING
            panel = self._makePanel(gui, cogIcons, suit, x)
            self.panels.append((panel, suit))
        gui.removeNode()
        cogIcons.removeNode()

    def _makePanel(self, gui, cogIcons, suit, x):
        frame = DirectFrame(
            parent=aspect2d,
            relief=None,
            frameSize=(-PANEL_W, PANEL_W, -PANEL_H, PANEL_H),
            image=gui.find('**/ToonBtl_Status_BG'),
            image_scale=(PANEL_W * 5.5, 1, PANEL_H * 5.5),
            image_color=PANEL_COLOR,
            pos=(x, 0, 0.55),
        )
        # Cog head - top-right portrait square
        headNode = frame.attachNewNode('head')
        for part in suit.headParts:
            copyPart = part.copyTo(headNode)
            copyPart.setDepthTest(1)
            copyPart.setDepthWrite(1)
        p1 = Point3()
        p2 = Point3()
        headNode.calcTightBounds(p1, p2)
        d = p2 - p1
        biggest = max(d[0], d[1], d[2]) or 1
        s = 0.12 / biggest
        headNode.setPosHprScale(0.12, 0, 0.02, 180, 0, 0, s, s, s)
        # HP label - left side, upper
        hpLabel = DirectLabel(
            parent=frame,
            relief=None,
            pos=(-0.07, 0, 0.06),
            text='%d/%d' % (int(suit.currHP), int(suit.maxHP)),
            text_scale=0.042,
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 0.8),
        )
        # Department icon - center between HP and level
        dept = suit.dna.dept if suit.dna else 'c'
        iconName = DEPT_ICONS.get(dept, 'CorpIcon')
        iconGeom = cogIcons.find('**/' + iconName)
        if not iconGeom.isEmpty():
            iconNode = frame.attachNewNode('deptIcon')
            iconGeom.copyTo(iconNode)
            iconNode.setDepthTest(1)
            iconNode.setDepthWrite(1)
            iconNode.setColor(DEPT_ICON_COLORS.get(dept, Vec4(1, 1, 1, 1)))
            ip1 = Point3()
            ip2 = Point3()
            iconNode.calcTightBounds(ip1, ip2)
            id_ = ip2 - ip1
            ibiggest = max(id_[0], id_[1], id_[2]) or 1
            iconNode.setScale(0.10 / ibiggest)
            iconNode.setPos(-0.07, 0, -0.015)
        # Level label - left side, lower
        lvlText = 'Lv. %d' % suit.getActualLevel()
        if suit.executive:
            lvlText += ' .exe'
        DirectLabel(
            parent=frame,
            relief=None,
            pos=(-0.07, 0, -0.09),
            text=lvlText,
            text_scale=0.048,
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 0.8),
        )
        frame.hpLabel = hpLabel
        return frame

    def update(self):
        for frame, suit in self.panels:
            frame.hpLabel['text'] = '%d/%d' % (int(suit.currHP), int(suit.maxHP))

    def hideAll(self):
        for frame, suit in self.panels:
            frame.hide()

    def showAll(self):
        for frame, suit in self.panels:
            frame.show()

    def destroy(self):
        for frame, suit in self.panels:
            frame.destroy()
        self.panels = []
