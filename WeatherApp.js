<!DOCTYPE html>
<html>
  <head>
    <title>To-Do List</title>
    <style>
      input[type="text"] {
        width: 75%;
        padding: 12px 20px;
        margin: 8px 0;
        box-sizing: border-box;
        border: 2px solid #ccc;
        border-radius: 4px;
      }

      input[type="submit"] {
        background-color: #4caf50;
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }

      input[type="submit"]:hover {
        background-color: #45a049;
      }

      .item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 10px;
        margin: 10px 0;
        border: 1px solid #ccc;
        border-radius: 4px;
      }

      .item p {
        margin: 0;
        flex-grow: 1;
        padding-right: 10px;
      }

      .item button {
        background-color: #f44336;
        color: white;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }

      .item button:hover {
        background-color: #e53935;
      }
    </style>
  </head>
  <body>
    <h1>To-Do List</h1>
    <form>
      <input type="text" id="newItem" placeholder="Enter a new item...">
      <input type="submit" value="Add" onclick="addItem()">
    </form>
    <div id="itemList"></div>

    <script>
      let items = [];

      function addItem() {
        const newItem = document.getElementById("newItem");
        const itemList = document.getElementById("itemList");

        items.push(newItem.value);

        const itemIndex = items.length - 1;
        const item = document.createElement("div");
        item.setAttribute("class", "item");
        item.innerHTML = `
          <p>${items[itemIndex]}</p>
          <button onclick="deleteItem(${itemIndex})">Delete</button>
        `;

        itemList.appendChild(item);

        newItem.value = "";
      }

      function deleteItem(index) {
        const itemList = document.getElementById("itemList");
        itemList.removeChild(itemList.childNodes[index]);
        items.splice(index, 1);
      }
    </script>
  </body>
</html>
