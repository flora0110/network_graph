const Graph = ForceGraph3D()
  (document.getElementById('3d-graph'))
    .jsonUrl('https://raw.githubusercontent.com/flora0110/network_graph/master/node_and_link.json')
    .nodeColor('color')
    .nodeThreeObject(node => {
      const sprite = new SpriteText(node.id);
      sprite.material.depthWrite = false; // make sprite background transparent
      sprite.color =node.color;
      sprite.textHeight = node.group;
      return sprite;
    })
    .linkThreeObjectExtend(true)
    .linkThreeObject(link => {
      // extend link with text sprite
      const sprite = new SpriteText(`${link.source} > ${link.target}`);
      sprite.color = 'white';
      sprite.textHeight = 1.5;
      return sprite;
    })
    .linkPositionUpdate((sprite, { start, end }) => {
      const middlePos = Object.assign(...['x', 'y', 'z'].map(c => ({
        [c]: start[c] + (end[c] - start[c]) / 2 // calc middle point
      })));
      // Position sprite
      Object.assign(sprite.position, middlePos);
    })
    .linkWidth ('value');

// Spread nodes a little wider
Graph.d3Force('charge').strength(-120);
