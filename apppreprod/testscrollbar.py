import sys
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem, QVBoxLayout, QWidget

class MonApplication(QApplication):
    def __init__(self, argv):
        super(MonApplication, self).__init__(argv)

        # Créer l'interface graphique
        self.fenetre_principale = QWidget()
        layout = QVBoxLayout(self.fenetre_principale)

        self.packet_tree = QTreeWidget(self.fenetre_principale)
        self.packet_tree.setHeaderLabels(['ID', 'IP SRC', 'IP DST', 'INFO'])

        # Ajouter des éléments à l'arborescence (c'est un exemple, à remplacer par vos données réelles)
        self.ajouter_element_arborescence("1", "192.168.1.1", "192.168.1.2", "Informations 1")
        self.ajouter_element_arborescence("2", "192.168.1.3", "192.168.1.4", "Informations 2")

        # Connecter le signal itemDoubleClicked à une fonction
        self.packet_tree.itemDoubleClicked.connect(self.item_double_clicked)

        # Ajouter l'arborescence au layout
        layout.addWidget(self.packet_tree)

        # Afficher la fenêtre principale
        self.fenetre_principale.show()

    def ajouter_element_arborescence(self, id, ip_src, ip_dst, info):
        item = QTreeWidgetItem(self.packet_tree, [id, ip_src, ip_dst, info])
        return item

    def item_double_clicked(self, item, column):
        # Fonction appelée lorsqu'un élément de l'arborescence est double-cliqué
        print("Double clic sur l'élément:", item.text(column))

if __name__ == '__main__':
    app = MonApplication(sys.argv)
    sys.exit(app.exec_())