// frontend/src/Chat.js
import React, {useEffect, useState, useRef} from "react";
import { WS_URL, BOT_EMAIL } from "./config";

export default function Chat({user}) {
  const [messages, setMessages] = useState([]);
  const wsRef = useRef(null);

  useEffect(()=>{
    const ws = new WebSocket(`${WS_URL}/ws/${encodeURIComponent(user.email)}?token=${user.token}`);
    ws.onopen = ()=> console.log("ws open");
    ws.onmessage = (ev)=>{
      const d = JSON.parse(ev.data);
      if (d.type === "new_message") setMessages(m=>[...m, d.message]);
    };
    ws.onclose = ()=> console.log("ws closed");
    wsRef.current = ws;
    return ()=> ws.close();
  },[user.email, user.token]);

  function sendMessage(recipient, content){
    const payload = {type:"message", payload:{sender:user.email, recipient, content}};
    wsRef.current.send(JSON.stringify(payload));
    // also optional: add to local UI immediately
    setMessages(m=>[...m, {sender:user.email, recipient, content, timestamp: new Date(), is_bot_response:false}]);
  }

  return (
    <div>
      <div aria-live="polite">
        {messages.map((m,i)=>(<div key={i}><b>{m.sender}</b>: {m.content}</div>))}
      </div>
      <div>
        <button onClick={()=>sendMessage(BOT_EMAIL,"hi")}>Say hi to bot</button>
        <input id="msgbox" />
        <button onClick={()=>{
          const txt = document.getElementById("msgbox").value;
          sendMessage(BOT_EMAIL, txt);
        }}>Send</button>
      </div>
    </div>
  );
}
