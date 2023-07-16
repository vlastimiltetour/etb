from django.shortcuts import render


def payment_process(request):
    # Add your payment processing logic here
    context = ""
    return render(request, "payments/process.html", {"context": context})


def payment_completed(request):
    return render(request, "payments/completed.html")


def payment_canceled(request):
    return render(request, "payments/canceled.html")
