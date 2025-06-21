import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [cards, setCards] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/cards')
      .then(res => {
        setCards(res.data.items); // 'items' contains the card list
      })
      .catch(err => console.error(err));
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Clash Royale Cards</h1>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {cards.map(card => (
          <div key={card.id} className="bg-white shadow-md p-4 rounded">
            <img src={card.iconUrls.medium} alt={card.name} className="w-full h-32 object-contain mb-2" />
            <h2 className="text-lg font-semibold">{card.name}</h2>
            <p>Rarity: {card.rarity}</p>
            <p>Elixir Cost: {card.elixirCost}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;

