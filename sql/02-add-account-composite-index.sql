/*
 *  /*************************************************************************
 *  *
 *  * AMIT KUMAR KHETAN CONFIDENTIAL
 *  * __________________
 *  *
 *  *  [2017] - [2021] Amit Kumar Khetan
 *  *  All Rights Reserved.
 *  *
 *  * NOTICE:  All information contained herein is, and remains
 *  * the property of Amit Kumar Khetan and its suppliers,
 *  * if any.  The intellectual and technical concepts contained
 *  * herein are proprietary to Amit Kumar Khetan
 *  * and its suppliers and may be covered by U.S. and Foreign Patents,
 *  * patents in process, and are protected by trade secret or copyright law.
 *  * Dissemination of this information or reproduction of this material
 *  * is strictly forbidden unless prior written permission is obtained
 *  * from Amit Kumar Khetan.
 *
 */
*/

-- Add a composite index for account_country_code and account_mobile_number
CREATE INDEX idx_account_country_mobile
    ON Account (account_country_code, account_mobile_number);
