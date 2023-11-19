#   /*************************************************************************
#   *
#   * AMIT KUMAR KHETAN CONFIDENTIAL
#   * __________________
#   *
#   *  [2017] - [2021] Amit Kumar Khetan
#   *  All Rights Reserved.
#   *
#   * NOTICE:  All information contained herein is, and remains
#   * the property of Amit Kumar Khetan and its suppliers,
#   * if any.  The intellectual and technical concepts contained
#   * herein are proprietary to Amit Kumar Khetan
#   * and its suppliers and may be covered by U.S. and Foreign Patents,
#   * patents in process, and are protected by trade secret or copyright law.
#   * Dissemination of this information or reproduction of this material
#   * is strictly forbidden unless prior written permission is obtained
#   * from Amit Kumar Khetan.
#   */

import stripe


def createOrganizationPayIn():
    organization_country = "IN"
    organization_pay_in = stripe.Account.create(
        country=organization_country,
        type='custom',
        capabilities={
            'card_payments': {
                'requested': True,
            },
            'transfers': {
                'requested': True,
            },
        },
    )
    # todo: we need to store meta information about this connected account somewhere


def organization_identity_verification():
    # address is needed
    # date of birth is needed

    # need to accept terms of service
    # with Datetime and IP of the user

    # this will be based on country
    # for INDIA
    # accepted IDENTITY VERIFICATION documents are:
    # Passport, PAN CARD, Driver's License, Voter ID Card (scans of front and back are required)

    # accepted Address Proof are Voter ID Card (scans of front and back are required)

    # company/entity documents
    # PAN Card or (Articles of Incorporation)

    pass
