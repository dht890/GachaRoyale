import { useState } from "react";
import axios from "axios";

export default function CreateUserForm() {
  const [username, setUsername] = useState("");
  const [lvl, setLvl] = useState(1);
  const [pfp, setPfp] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post("http://localhost:5000/user", {
        username,
        lvl,
        pfp,
      });
      alert("User created successfully!");
      console.log(res.data);
    } catch (err) {
      console.error(err);
      alert("Failed to create user");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 max-w-md mx-auto space-y-4">
      <h2 className="text-xl font-bold">Create User</h2>
      <input
        type="text"
        placeholder="Username"
        value={username}
        className="w-full border p-2 rounded"
        onChange={(e) => setUsername(e.target.value)}
        required
      />
      <input
        type="number"
        placeholder="Level"
        value={lvl}
        className="w-full border p-2 rounded"
        onChange={(e) => setLvl(parseInt(e.target.value))}
        min={1}
        required
      />
      <input
        type="text"
        placeholder="Profile Picture URL"
        value={pfp}
        className="w-full border p-2 rounded"
        onChange={(e) => setPfp(e.target.value)}
      />
      <button type="submit" className="bg-blue-500 text-white px-4 py-2 rounded">
        Create
      </button>
    </form>
  );
}
