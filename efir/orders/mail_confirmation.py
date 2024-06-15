<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8" />
		<title>Prodejní doklad / faktura č. {{order.etb_id}}</title>

		<style>
			.invoice-box {
				max-width: 800px;
				margin: auto;
				padding: 30px;
				border: 1px solid #eee;
				box-shadow: 0 0 10px rgba(0, 0, 0, 0.15);
				font-size: 12px;
				line-height: 24px;
				font-family: 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
				color: #555;
			}

			.invoice-box table {
				width: 100%;
				line-height: inherit;
				text-align: left;
			}

			.invoice-box table td {
				padding: 5px;
				vertical-align: top;
			}

			.invoice-box table tr td:nth-child(2) {
				text-align: right;
			}

			.invoice-box table tr.top table td {
				padding-bottom: 20px;
			}

			.invoice-box table tr.top table td.title {
				font-size: 45px;
				line-height: 45px;
				color: #333;
			}

			.invoice-box table tr.information table td {
				padding-bottom: 40px;
			}

			.invoice-box table tr.heading td {
				background: #eee;
				border-bottom: 1px solid #ddd;
				font-weight: bold;
			}

			.invoice-box table tr.details td {
				padding-bottom: 20px;
			}

			.invoice-box table tr.item td {
				border-bottom: 1px solid #eee;
			}

			.invoice-box table tr.item.last td {
				border-bottom: none;
			}

			.invoice-box table tr.total td:nth-child(2) {
				border-top: 2px solid #eee;
				font-weight: bold;
			}

			@media only screen and (max-width: 600px) {
				.invoice-box table tr.top table td {
					width: 100%;
					display: block;
					text-align: center;
				}

				.invoice-box table tr.information table td {
					width: 100%;
					display: block;
					text-align: center;
				}
			}

			/** RTL **/
			.invoice-box.rtl {
				direction: rtl;
				font-family: Tahoma, 'Helvetica Neue', 'Helvetica', Helvetica, Arial, sans-serif;
			}

			.invoice-box.rtl table {
				text-align: right;
			}

			.invoice-box.rtl table tr td:nth-child(2) {
				text-align: left;
			}
		</style>
	</head>

	<body>
		<div class="invoice-box">
			<table cellpadding="0" cellspacing="0">
				<tr class="top">
					<td colspan="2">
						<table>
							<tr>
								<td class="title">
									<img
										
										src="https://live.staticflickr.com/65535/53285987159_99d65a33b9_k.jpg" type="image"

										style="width: 100%; max-width: 150px"
									/>
								</td>
							<tr>
								<td>
									Faktura #{{ order.etb_id }}<br>
									Datum vystavení: {{ order.created }} <br>
									Datum uskutečnění plnění:  {{ order.created }} <br>

								</td>
							</tr>
							</tr>
						</table>
					</td>
				</tr>

				<tr class="information">
					<td colspan="2">
						<table>
							<tr>
								<td>
									<u>Prodávající:</u><br>
									Ing. Valeriya Ageeva<br>
									Sídlo: Příčná 1892/4, 110 00, Praha 1 - Nové Město<br>
									IČ:17092540<br>
									číslo účtu: 2270534028/3030<br>
									IBAN: CZ79 3030 0000 0022 7053 4028<br>
									SWIFT: AIRACZPP<br>
									e-mail: objednavky@efirthebrand.cz<br>
									Tel. č.: +420774363883<br>
									<br>
									Není plátcem DPH


								
								</td>

								<td>
									<u>Kupující:</u> <br>
									
									Jméno a příjmení / Název firmy: {{ order.first_name }} {{ order.last_name }}<br>
									Dodací adresa: {{ order.address }}, {{ order.city }}, {{order.postcode}}, {{ order.country}} <br>
									Email: {{ order.email }} <br/>
									Tel. č {{ order.number }} 

									
									
									
								</td>
							</tr>
						</table>
					</td>
				</tr>

				
				


				<tr class="heading">
					<td>Položka</td>

					<td>Cena</td>
				</tr>

				{% for item in order.items.all %}
				<tr class="item">
					<td>{{ item.product.name }} </td>

					<td> {{ item.price }} Kč</td>
				</tr>
				{% endfor %}

				<tr></tr>


				<tr class="item">
					<td>Doprava </td>

					<td> {{ order.shipping_price }} Kč
					</td>
				</tr>
				{% if order.discount > 0 %}

				<tr class="item">
					<td>Sleva </td>

					<td>-{{ order.discount }} Kč
					</td>
				</tr>
				{% endif %}


						
					<tr class="total">
						<td></td>

					<td>Total: {{ order.total_cost }} Kč</td>
				</tr>
			</table>
			<br>
			Forma platby: Platba provedena skrz platební bránu Stripe.
		</div>
	</body>
</html>
