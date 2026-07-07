export default function Chat() {
  return (
    <div className="flex flex-col h-full">

      <div className="flex-1 overflow-y-auto space-y-3">

        <div className="bg-white p-3 rounded-xl w-fit max-w-[80%]">
          Hello 👋
        </div>

        <div className="bg-green-200 p-3 rounded-xl ml-auto w-fit max-w-[80%]">
          Should I water my plant?
        </div>

      </div>

      
      <div className="flex flex-col sm:flex-row gap-2 mt-4">

        <input
          className="border p-3 rounded-xl flex-1"
          placeholder="Ask your plant doctor..."
        />

        <button className="bg-green-600 text-white px-6 py-3 rounded-xl">
          Send
        </button>

      </div>

    </div>
  );
}