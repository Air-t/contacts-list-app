import os

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views import View
from contacts.forms import PersonForm, AddressForm, EmailForm, PhoneForm, GroupForm, SelectGroupForm, ShortPersonForm
from contacts.models import Person, Address, Email, Phone, Group


def goto(request):
    return redirect('contacts:contact_list')


class ContactList(View):
    def get(self, request):
        contacts = Person.objects.all().order_by('surname')
        form = ShortPersonForm()
        return render(request, 'contacts/contact_list.html', {'form': form, 'contacts': contacts})

    def post(self, request):

        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contact has been created.')
            return redirect('contacts:contact_list')
        else:
            messages.error(request, 'While adding new contact an error has occurred.')
            return redirect('contacts:contact_list')


class DeleteContactView(View):
    def post(self, request, id):
        person = get_object_or_404(Person, pk=id)
        person.delete()
        messages.success(request, 'Contact deleted.')
        return redirect('contacts:contact_list')


class PersonView(View):
    def get(self, request, id):
        person = Person.objects.get(pk=id)
        return render(request, 'contacts/contact_details.html', {'contact': person,
                                                                 'form': PersonForm(instance=person),
                                                                 'group_form': GroupForm(),
                                                                 'join_group_form': SelectGroupForm(person=person),
                                                                 'person_groups': person.group_set.all(),
                                                                 'groups': Group.objects.all(),
                                                                 'addresses': person.address_set.all(),
                                                                 'emails': person.email_set.all(),
                                                                 'phones': person.phone_set.all(),
                                                                 })

    def post(self, request, id):
        person = Person.objects.get(pk=id)
        img_path = person.photo.path
        form = PersonForm(request.POST or None, request.FILES or None, instance=person)
        action = request.POST.get('action')
        if action is not None:
            if action == 'delete_address':
                object = Address.objects.get(pk=int(request.POST.get('id')))
            elif action == 'delete_email':
                object = Email.objects.get(pk=int(request.POST.get('id')))
            elif action == 'delete_phone':
                object = Phone.objects.get(pk=int(request.POST.get('id')))
            object.delete()
            return redirect('contacts:contact', id=id)

        if form.is_valid():
            if request.POST.get('photo-clean'):
                os.remove(img_path)
            else:
                form.photo = img_path
            form.save()
            messages.success(request, "Contact was updated")
            return redirect('contacts:contact', id=id)
        else:
            messages.warning(request, 'While updating contact an error has occurred.')
        return render(request, 'contacts/contact_details.html', {'contact': person, 'form': form})


class AddPersonAddress(View):
    def get(self, request, id):
        form = AddressForm()
        return render(request, 'contacts/address.html', {'form': form})

    def post(self, request, id):
        form = AddressForm(data=request.POST)
        if form.is_valid():
            person = Person.objects.get(pk=id)
            address = form.save(commit=False)
            address.person = person
            address.save()
            messages.success(request, "Address was added")
            return redirect('contacts:contact', id=id)
        else:
            messages.warning(request, 'While updating contact an error has occurred.')
        return redirect('contacts:contact', id=id)


class ModifyPersonAddress(View):

    def get(self, request, id, address_id):
        person = get_object_or_404(Person, pk=id)
        address = get_object_or_404(Address, pk=address_id)
        form = AddressForm(instance=address)
        return render(request, 'contacts/address.html', {'form': form})

    def post(self, request, id, address_id):
        address = get_object_or_404(Address, pk=address_id)
        form = AddressForm(data=request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, "Address was updated")
            return redirect('contacts:contact', id=id)
        else:
            messages.warning(request, 'While updating address an error has occurred.')
        return redirect('contacts:contact', id=id)


class AddPersonEmail(View):
    def get(self, request, id):
        return render(request, 'contacts/email.html', {'form': EmailForm()})

    def post(self, request, id):
        form = EmailForm(data=request.POST)
        if form.is_valid():
            person = Person.objects.get(pk=id)
            email = form.save(commit=False)
            email.person = person
            email.save()
            messages.success(request, "Email was added")
            return redirect('contacts:contact', id=id)
        else:
            messages.warning(request, 'While updating email an error has occurred.')
        return redirect('contacts:contact', id=id)


class ModifyPersonEmail(View):
    def get(self, request, id, email_id):
        email = get_object_or_404(Email, pk=email_id)
        form = EmailForm(instance=email)
        return render(request, 'contacts/email.html', {'form': form})

    def post(self, request, id, email_id):
        email = get_object_or_404(Email, pk=email_id)
        form = EmailForm(data=request.POST, instance=email)
        if form.is_valid():
            form.save()
            messages.success(request, "Email was updated")
            return redirect('contacts:contact', id=id)
        else:
            messages.warning(request, 'While updating email an error has occurred.')
        return redirect('contacts:contact', id=id)


class AddPersonPhone(View):
    def get(self, request, id):
        form = PhoneForm()
        return render(request, 'contacts/phone.html', {'form': form})

    def post(self, request, id):
        form = PhoneForm(data=request.POST)
        if form.is_valid():
            person = Person.objects.get(pk=id)
            phone = form.save(commit=False)
            phone.person = person
            phone.save()
            messages.success(request, "Phone was added")
            return redirect('contacts:contact', id=id)
        else:
            messages.warning(request, 'While updating phone an error has occurred.')
        return redirect('contacts:contact', id=id)


class ModifyPersonPhone(View):

    def get(self, request, id, phone_id):
        person = get_object_or_404(Person, pk=id)
        phone = get_object_or_404(Phone, pk=phone_id)
        form = PhoneForm(instance=phone)
        return render(request, 'contacts/phone.html', {'form': form})

    def post(self, request, id, phone_id):
        phone = get_object_or_404(Email, pk=phone_id)
        form = PhoneForm(data=request.POST, instance=phone)
        if form.is_valid():
            form.save()
            messages.success(request, "Phone was updated")
            return redirect('contacts:contact', id=id)
        else:
            messages.warning(request, 'While updating phone an error has occurred.')
        return redirect('contacts:contact', id=id)


class GroupsView(View):
    def get(self, request):
        return render(request, 'contacts/groups.html', {'groups': Group.objects.all().order_by('name')})

    def post(self, request):
        if request.POST.get('action') == 'delete':
            group = Group.objects.get(pk=int(request.POST.get('id')))
            # todo delete all relevent group markers in contacts
            group.delete()
            messages.success(request, 'Group was deleted.')
        return redirect('contacts:groups')


class GroupView(View):
    def get(self, request, id):
        group = get_object_or_404(Group, pk=id)
        contacts = group.person.all()
        return render(request, 'contacts/group_details.html', {'group': group, 'contacts': contacts})


class AddGroupView(View):
    def post(self, request):
        form = GroupForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Group was created.")
            return redirect('contacts:groups')
        else:
            messages.error(request, 'Can not create group.')
        return redirect('contacts:groups')


class ModifyGroupView(View):
    def get(self, request, group_id):
        form = GroupForm(instance=get_object_or_404(Group, pk=group_id))
        return render(request, 'contacts/group.html', {'form': form})

    def post(self, request, group_id):
        form = GroupForm(instance=get_object_or_404(Group, pk=group_id), data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Group name was renamed.")
            return redirect('contacts:groups')
        form.add_error('name', 'Please provide different name.')
        messages.warning(request, 'An error has occurred.')
        render(request, 'contacts/group.html', {'form': form})


class AddToGroupView(View):
    def post(self, request, id):
        action = request.POST.get("action")
        person = Person.objects.get(pk=id)
        if action == "Create":
            form = GroupForm(data=request.POST)
            if form.is_valid():
                group = form.save(commit=False)
                group.save()
                person.group_set.add(group)
                messages.success(request, f"Group {group.name} was created.")
                return redirect('contacts:contact', id=id)
        else:
            form = SelectGroupForm(data=request.POST)
            if form.is_valid():
                groups = form.cleaned_data.get('group')
                [person.group_set.add(group) for group in groups]
                [messages.success(request, f"{person.name} has joined {group.name}.") for group in groups]
                return redirect('contacts:contact', id=id)
            else:
                messages.warning(request, 'An error has occurred.')
        return redirect('contacts:contact', id=id)


class RemoveFromGroupView(View):
    def post(self, request):
        group = get_object_or_404(Group, pk=request.POST.get('id'))
        person = get_object_or_404(Person, pk=request.POST.get('person_id'))
        person.group_set.remove(group)
        messages.success(request, f"{person.name} has been removed from {group.name}.")
        return redirect('contacts:contact', id=request.POST.get('person_id'))


class SearchGroupView(View):
    def post(self, request, id):
        group = get_object_or_404(Group, pk=id)
        contacts = group.person.all()
        name = request.POST.get('search')
        names = contacts.filter(name__icontains=name)
        surnames = contacts.filter(surname__icontains=name)
        results = names.union(surnames)
        if results.count() != 0:
            messages.success(request, f"{results.count()} contacts found!")
        else:
            messages.warning(request, f"No contacts found this time.")
        return render(request, 'contacts/search.html', {'contacts': results, 'group': group})
