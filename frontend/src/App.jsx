import React from "react";
import UploadForm from "./components/UploadForm";
import Type0 from "./components/result/Type0";

function App() {
  
  return (
    <div className="App bg-[#282b2e]">
      <header className="p-6 text-[#1DB954]">
        <h2 className="text-left kanit-bold text-2xl">SpotiType</h2>
      </header>
      <main className="bg-[url(../public/bg.png)] text-gray-100 px-6 py-40">
        <h1 className="kanit-black text-7xl mb-8">What <span className="text-[#1DB954]">type</span> of listener are you?</h1>
        <p className="font-semibold text-2xl text-gray-300">Discover what your favorite songs tell about you!</p>
      </main>
      <section className="pt-10 pb-20">
        <UploadForm />
      </section>
      <section className="pt-10 pb-20">
        <Type0 />
      </section>
      <footer className="pt-10 pb-2 text-white bg-[#1DB954]">
        <p>SpotiType - Project by <a href="https://elenazen.it" className="text-white underline">Elena Zen</a></p>
      </footer>
    </div>
  );
}

export default App;