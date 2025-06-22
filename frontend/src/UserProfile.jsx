import { useEffect, useState } from "react";
import axios from "axios";

export default function UserProfile({ username }) {
  const [user, setUser] = useState(null);

  useEffect(() => {
    axios.get(`http://localhost:5000/user/${username}`)
      .then(res => setUser(res.data))
      .catch(err => console.error("User not found"));
  }, [username]);

  if (!user) return <p>Loading profile...</p>;

  return (
    <div className="p-4 max-w-md mx-auto text-center">
      <img src={user.pfp} alt="Profile" className="w-24 h-24 rounded-full mx-auto mb-4" />
      <h2 className="text-2xl font-bold">{user.username}</h2>
      <p>Level: {user.lvl}</p>
    </div>
  );
}
