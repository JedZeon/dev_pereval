Итоговая аттестация (виртуальная стажировка) SkillFactory.
Спринт/Задание по созданию Rest API в рамках совместной разработки мобильного приложения
для Android и IOS ФСТР (Федерации Спортивного Туризма России).

<div style="border-left: 5px solid #00b43f; padding-left: 10px;">
<h3><strong>Методы <em>REST</em> <em>API</em>:</strong></h3>
</div>

<ul>
<ul>
<li><strong style="color: #00b43f;"><em>POST</em> /<em>submitData</em></strong> — метод <em>submitData </em>принимает <em>JSON</em> в теле запроса с информацией о перевале. Ниже находится пример такого <em>JSON</em>-а.</li>
<li><strong style="color: #00b43f;"><em>GET</em> /<em>submitData</em>/&lt;<em>id</em>&gt;</strong> — получить одну запись (перевал) по её <em>id</em>.<br>Получает всю информацию об объекте, в том числе статус модерации.</li>
<li><strong style="color: #00b43f;"><em>PATCH</em> /<em>submitData</em>/&lt;<em>id</em>&gt;</strong> — отредактировать существующую запись (замена), если она в статусе <em>new</em>.<br>Редактировать можно все поля, кроме тех, что содержат в себе ФИО, адрес почты и номер телефона. Метод принимает тот же самый <em>json</em>, который принимал уже реализованный тобой метод <em>submitData</em>.<br><br>В качестве результата возвращает значение:
<ul>
<ul>
<li><strong style="color: #00b43f;"><em>state</em></strong>:
<ul>
<ul>
<li><strong style="color: #00b43f;">1</strong> — если успешно удалось отредактировать запись в базе данных.</li>
<li><strong style="color: #00b43f;">0</strong> — в противном случае.</li>
</ul>
</ul>
</li>
<li><strong style="color: #00b43f;"><em>message</em> </strong>— если обновить запись не удалось, описывается причина.</li>
</ul>
</ul>
</li>
<li><strong style="color: #00b43f;"><em>GET</em> /<em>submitData</em>/?<em>user</em>__<em>email</em>=&lt;<em>email</em>&gt;</strong> — список данных обо всех объектах, которые пользователь с почтой <em>&lt;email&gt;</em> отправил на сервер.</li>
</ul>
</ul>



<div style="border-left: 5px solid #00b43f; padding-left: 10px;">
<h3><strong>Метод <em>POST submitData</em></strong></h3>
</div>

Когда турист поднимется на перевал, он сфотографирует его и внесёт нужную информацию с помощью мобильного приложения:

<ul>
<ul>
<li>координаты объекта и его высоту;</li>
<li>название объекта;</li>
<li>несколько фотографий;</li>
<li>информацию о пользователе, который передал данные о перевале:
<ul>
<ul>
<li>имя пользователя (ФИО строкой);</li>
<li>почта;</li>
<li>телефон.</li>
</ul>
</ul>
</li>
</ul>
</ul>
<p>После этого турист нажмёт кнопку «Отправить» в мобильном приложении. Мобильное приложение вызовет метод&nbsp;<strong style="color: #00b43f;"><em>submitData </em></strong><span style="font-size: 1em;">твоего </span><em style="font-size: 1em;">REST</em><span style="font-size: 1em;"> </span><em style="font-size: 1em;">API</em><span style="font-size: 1em;">.</span></p>

<p>Метод <em>submitData </em>принимает <em>JSON</em> в теле запроса с информацией о перевале. Ниже находится пример такого <em>JSON</em>-а:</p>
<div style="overflow: auto; width: auto; border: solid #D1D9D7; border-width: .1em; padding: .2em .6em;">
<pre style="margin: 0; line-height: 125%;" class="hljs language-css">{
  "beauty_title": <span class="hljs-string">"пер. "</span>,
  <span class="hljs-string">"title"</span>: <span class="hljs-string">"Пхия"</span>,
  <span class="hljs-string">"other_titles"</span>: <span class="hljs-string">"Триев"</span>,
  <span class="hljs-string">"connect"</span>: <span class="hljs-string">""</span>, // что соединяет, текстовое поле

<span class="hljs-string">"add_time"</span>: <span class="hljs-string">"2021-09-22 13:18:13"</span>,
<span class="hljs-string">"user"</span>: {"email": <span class="hljs-string">"qwerty@mail.ru"</span>, 		
<span class="hljs-string">"fam"</span>: <span class="hljs-string">"Пупкин"</span>,
<span class="hljs-string">"name"</span>: <span class="hljs-string">"Василий"</span>,
<span class="hljs-string">"otc"</span>: <span class="hljs-string">"Иванович"</span>,
<span class="hljs-string">"phone"</span>: <span class="hljs-string">"+7 555 55 55"</span>},

"coords":{
"latitude": <span class="hljs-string">"45.3842"</span>,
<span class="hljs-string">"longitude"</span>: <span class="hljs-string">"7.1525"</span>,
<span class="hljs-string">"height"</span>: <span class="hljs-string">"1200"</span>}

level:{"winter": <span class="hljs-string">""</span>, //Категория трудности. В разное время года перевал может иметь
разную категорию трудности
<span class="hljs-string">"summer"</span>: <span class="hljs-string">"1А"</span>,
<span class="hljs-string">"autumn"</span>: <span class="hljs-string">"1А"</span>,
<span class="hljs-string">"spring"</span>: <span class="hljs-string">""</span>},

images: [{data:<span class="hljs-string">"&lt;картинка1&gt;"</span>, title:<span class="hljs-string">"Седловина"</span>}, {data:<span class="hljs-string">"&lt;картинка&gt;"</span>, title:<span class="hljs-string">"Подъём"</span>}]
}
</pre>
</div>

<p>Результат метода: <em>JSON</em></p>
<ul>
<ul>
<ul>
<li><strong><em>status</em></strong> — код <em>HTTP</em>, целое число:
<ul>
<ul>
<li>500 — ошибка при выполнении операции;</li>
<li>400 — <em>Bad Request</em>&nbsp;<em>(при нехватке полей)</em>;</li>
<li>200 — успех.</li>
</ul>
</ul>
</li>
<li><strong><em>message</em> </strong>— строка:
<ul>
<li>Причина ошибки <em>(если она была)</em>;</li>
<li>Отправлено успешно;</li>
<li>Если отправка успешна, дополнительно возвращается <em>id</em> вставленной записи.</li>
</ul>
</li>
<li><strong><em>id</em> </strong>— идентификатор, который был присвоен объекту при добавлении в базу данных.</li>
</ul>
</ul>
</ul>

<p>Примеры ответа:</p>
<ul>
<ul>
<ul>
<li><code>{ "status": 500, "message": "Ошибка подключения к базе данных","id": null}</code></li>
<li><code>{ "status": 200, "message": null, "id": 42 }</code></li>
</ul>
</ul>
</ul>

<div style="border-left: 5px solid #00b43f; padding-left: 10px;">
<h3><strong>Возможные значения поля <em>status</em></strong></h3>
</div>
<ul dir="auto">
<li><em>'new' - новая запись;</em></li>
<li><em>'pending' — модератор взял в работу;</em></li>
<li><em>'accepted'  — модерация прошла успешно;</em></li>
<li><em>'rejected' — модерация прошла, информация не принята.</em></li>
</ul>

<div style="border-left: 5px solid #00b43f; padding-left: 10px;">
<h3><strong>Проект опубликован на хостинге <a href="https://sweb.ru/">spaceweb</a></strong></h3>
</div>
<ul dir="auto">
<li>Адрес API: <a href="pogr25.temp.swtest.ru">pogr25.temp.swtest.ru</a></li>
<li>Документация swagger: http://pogr25.temp.swtest.ru/swagger/</li>
<li>Документация redoc: http://pogr25.temp.swtest.ru/redoc/</li>
</ul>
