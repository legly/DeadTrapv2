import json
import requests
import phonenumbers
from phonenumbers import geocoder
from phonenumbers import carrier
from phonenumbers import timezone

def libphonenumbers(number):

    print('\n[*] Running local scan...\n')

    try:
        phonenumber = phonenumbers.parse(number, None)
    except:
        return False
    else:
        if not phonenumbers.is_valid_number(phonenumber):
            return False

        number = phonenumbers.format_number(phonenumber, phonenumbers.PhoneNumberFormat.E164).replace('+', '')
        numberCountryCode = phonenumbers.format_number(phonenumber, phonenumbers.PhoneNumberFormat.INTERNATIONAL).split(' ')[0]

        countryRequest = json.loads(requests.request('GET', 'https://restcountries.eu/rest/v2/callingcode/{}'.format(numberCountryCode.replace('+', ''))).content)
        numberCountry = countryRequest[0]['alpha2Code']

        localNumber = phonenumbers.format_number(phonenumber, phonenumbers.PhoneNumberFormat.E164).replace(numberCountryCode, '')
        internationalNumber = phonenumbers.format_number(phonenumber, phonenumbers.PhoneNumberFormat.INTERNATIONAL)

        print('[+] International format: {}'.format(internationalNumber))
        print('[+] Local format: 0{}'.format(localNumber))
        print('[+] Country code: {}'.format(numberCountryCode))
        print('[+] Location: {}'.format(geocoder.description_for_number(phonenumber, "en")))
        print('[+] Carrier: {}'.format(phonenumbers.carrier.name_for_number(phonenumber, 'en')))
        for libphonenumbers.timezoneResult in timezone.time_zones_for_number(phonenumber):
            print('[+] Timezone: {}'.format(libphonenumbers.timezoneResult))

        if phonenumbers.is_possible_number(phonenumber):
            print('[*] The number is valid and possible.')
        else:
            print('(!) The number is valid but might not be possible.')
