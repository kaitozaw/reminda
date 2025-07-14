const BASE_URL = "https://your-tunnel-name.trycloudflare.com";

function buildCustomerListCard(eventId, query = "") {
  const userEmail = getUserEmail_();  
  const url = `${BASE_URL}/api/customers?user_email=${encodeURIComponent(userEmail)}&query=${encodeURIComponent(query)}`;
  const result = fetchJsonSafe(url);
  if (!result.success) return buildErrorCard(result.message);
  const customers = result.data;

  const header = buildHeaderSection("default", {
    eventId: String(eventId)
  });

  const search = buildSearchSection(eventId, query, "customer_list");

  const body = CardService.newCardSection();
  if (customers.length === 0) {
    body.addWidget(
      CardService.newTextParagraph().setText("No customers.")
    );
  } else {
    customers.forEach(customer => {
      row = buildCustomerRow(customer, eventId, "available")
      body.addWidget(row);
    });
  }

  const card = CardService.newCardBuilder()
    .addSection(header)
    .addSection(search)
    .addSection(body)
    .build();
  
  return card
}

function buildCustomerDetailCard(e) {
  const userEmail = getUserEmail_();
  const customerId = e.commonEventObject.parameters.customerId;
  const eventId = e?.commonEventObject?.parameters?.eventId || "";
  const url = `${BASE_URL}/api/customers/${customerId}?user_email=${encodeURIComponent(userEmail)}`;
  const result = fetchJsonSafe(url);
  if (!result.success) return buildErrorCard(result.message);
  const customer = result.data;

  const header = buildHeaderSection("detail", {
    customerId: String(customer.id),
    eventId: String(eventId)
  });

  const subHeader = buildCustomerNameSection(customer, eventId);

  const body = buildCustomerDetailSection(customer);

  const card = CardService.newCardBuilder()
    .addSection(header)
    .addSection(subHeader)
    .addSection(body)
    .build();
  
  return card;
}

function buildAssignUnassignCard(eventId, activeTab = "assigned", query = "") {
  const header = buildHeaderSection("default", {
    eventId: String(eventId)
  });

  const search = (activeTab === "assigned")
    ? buildSearchSection(eventId, query, "assigned_customers")
    : buildSearchSection(eventId, query, "available_customers");  

  const tab = buildTabSection(eventId, activeTab);
  
  const body = (activeTab === "assigned")
    ? buildAssignedCustomersSection({commonEventObject: { parameters: { eventId, query} }})
    : buildAvailableCustomersSection({ commonEventObject: { parameters: { eventId, query } } });

  const card = CardService.newCardBuilder()
    .addSection(header)
    .addSection(search)
    .addSection(tab)
    .addSection(body)
    .build();

  return card;
}

function buildCreateCustomerCard(e) {
  const eventId = e?.commonEventObject?.parameters?.eventId || "";

  const header = buildHeaderSection("form", {
    eventId: String(eventId)
  });

  const body = CardService.newCardSection()
    .addWidget(CardService.newTextInput().setFieldName("first_name").setTitle("First Name"))
    .addWidget(CardService.newTextInput().setFieldName("last_name").setTitle("Last Name"))
    .addWidget(CardService.newTextInput().setFieldName("email").setTitle("Email"))
    .addWidget(CardService.newTextInput().setFieldName("tel").setTitle("Tel"))
    .addWidget(CardService.newTextInput().setFieldName("location").setTitle("Location"))
    .addWidget(CardService.newTextInput().setFieldName("description").setTitle("Description").setMultiline(true));

  const card = CardService.newCardBuilder()
    .addSection(header)
    .addSection(body)
    .build();
  
  return card;
}

function buildEditCustomerCard(e) {
  const userEmail = getUserEmail_();
  const customerId = e.commonEventObject.parameters.customerId || "";
  const eventId = e?.commonEventObject?.parameters?.eventId || "";
  const url = `${BASE_URL}/api/customers/${customerId}?user_email=${encodeURIComponent(userEmail)}`;
  const result = fetchJsonSafe(url);
  if (!result.success) return buildErrorCard(result.message);
  const customer = result.data;

  const header = buildHeaderSection("form", {
    eventId: String(eventId),
    customerId: String(customerId)
  });

  const body = CardService.newCardSection()
    .addWidget(CardService.newTextInput().setFieldName("first_name").setTitle("First Name").setValue(customer.first_name))
    .addWidget(CardService.newTextInput().setFieldName("last_name").setTitle("Last Name").setValue(customer.last_name))
    .addWidget(CardService.newTextInput().setFieldName("email").setTitle("Email").setValue(customer.email))
    .addWidget(CardService.newTextInput().setFieldName("tel").setTitle("Tel").setValue(customer.tel))
    .addWidget(CardService.newTextInput().setFieldName("location").setTitle("Location").setValue(customer.location))
    .addWidget(CardService.newTextInput().setFieldName("description").setTitle("Description").setValue(customer.description || "").setMultiline(true));

  const card = CardService.newCardBuilder()
    .addSection(header)
    .addSection(body)
    .build();
  
  return card;
}

function buildErrorCard(message) {
  const card = CardService.newCardBuilder()
    .setHeader(CardService.newCardHeader().setTitle("Error"))
    .addSection(
      CardService.newCardSection().addWidget(
        CardService.newTextParagraph().setText(message)
      )
    )
    .build();
  
  return card;
}

function buildHeaderSection(type, options = {}) {
  const section = CardService.newCardSection();

  if (type === "default") {    
    const webAppButton = CardService.newImageButton()
      .setAltText('Manage')
      .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/open_in_new_black_24dp.png")
      .setOpenLink(CardService.newOpenLink().setUrl(BASE_URL));

    section.addWidget(
      CardService.newKeyValue()
        .setTopLabel("Manage reminder")
        .setButton(webAppButton)
    );

    section.addWidget(CardService.newDivider());

    const createButton = CardService.newImageButton()
      .setAltText("Create customer")
      .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/add_black_24dp.png")
      .setOnClickAction(
        CardService.newAction()
          .setFunctionName("buildCreateCustomerCard")
          .setParameters({
            eventId: String(options.eventId || "")
          })
      );

    section.addWidget(
      CardService.newKeyValue()
        .setTopLabel("Create customer")
        .setButton(createButton)
    );
  }

  if (type === "form") {
    const isEdit = !!options.customerId;

    const saveButton = CardService.newImageButton()
      .setAltText("Save")
      .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/save_black_24dp.png")
      .setOnClickAction(
        CardService.newAction()
          .setFunctionName(isEdit ? "handleEditCustomerSubmit" : "handleCreateCustomerSubmit")
          .setParameters(
            Object.assign(
              { eventId: String(options.eventId || "") },
              isEdit ? { customerId: String(options.customerId) } : {}
            )
          )
      );

    section.addWidget(
      CardService.newKeyValue()
        .setTopLabel(isEdit ? "Update this customer" : "Create new customer")
        .setButton(saveButton)
    );
  }

  if (type === "detail") {
    const webAppButton = CardService.newImageButton()
      .setAltText('Manage')
      .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/open_in_new_black_24dp.png")
      .setOpenLink(CardService.newOpenLink().setUrl(BASE_URL));

    section.addWidget(
      CardService.newKeyValue()
        .setTopLabel("Manage reminder")
        .setButton(webAppButton)
    );

    section.addWidget(CardService.newDivider());
    
    const editButton = CardService.newImageButton()
      .setAltText("Edit")
      .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/edit_black_24dp.png")
      .setOnClickAction(
        CardService.newAction()
          .setFunctionName("buildEditCustomerCard")
          .setParameters({
            customerId: String(options.customerId),
            eventId: String(options.eventId || "")
          })
      );

    section.addWidget(
      CardService.newKeyValue()
        .setTopLabel("Edit this customer")
        .setButton(editButton)
    );

    const deleteButton = CardService.newImageButton()
      .setAltText("Delete")
      .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/delete_black_24dp.png")
      .setOnClickAction(
        CardService.newAction()
          .setFunctionName("handleDeleteCustomer")
          .setParameters({
            customerId: String(options.customerId),
            eventId: String(options.eventId || "")
          })
      );

    section.addWidget(
      CardService.newKeyValue()
        .setTopLabel("Delete this customer")
        .setButton(deleteButton)
    );
  }

  return section;
}

function buildSearchSection(eventId, query = "", source = "customer_list") {
  const section = CardService.newCardSection();

  section.addWidget(
    CardService.newTextInput()
      .setFieldName("query")
      .setValue(query)
  );

  const searchButton = CardService.newImageButton()
    .setAltText("Search")
    .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/search_black_24dp.png")
    .setOnClickAction(
      CardService.newAction()
        .setFunctionName("handleSearchAction")
        .setParameters({
          eventId: String(eventId),
          source: source
        })
    );

  section.addWidget(
    CardService.newKeyValue()
      .setTopLabel("Search customers")
      .setButton(searchButton)
  );

  return section;
}

function buildTabSection(eventId, activeTab = "assigned") {
  const section = CardService.newCardSection();

  const tabButtons = CardService.newButtonSet()
    .addButton(
      CardService.newTextButton()
        .setText("Assigned")
        .setTextButtonStyle(
          activeTab === "assigned"
            ? CardService.TextButtonStyle.FILLED
            : CardService.TextButtonStyle.TEXT
        )
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName("handleTabSwitch")
            .setParameters({
              eventId: String(eventId),
              tab: "assigned"
            })
        )
    )
    .addButton(
      CardService.newTextButton()
        .setText("Available")
        .setTextButtonStyle(
          activeTab === "available"
            ? CardService.TextButtonStyle.FILLED
            : CardService.TextButtonStyle.TEXT
        )
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName("handleTabSwitch")
            .setParameters({
              eventId: String(eventId),
              tab: "available"
            })
        )
    );

  section.addWidget(tabButtons);

  return section;
}

function buildCustomerNameSection(customer, eventId = "") {
  const section = CardService.newCardSection();

  const userEmail = getUserEmail_();
  const text = `${customer.first_name} ${customer.last_name}`;

  if (!eventId) {
    section.addWidget(CardService.newDecoratedText().setText(text).setWrapText(true));
    return section;
  }

  const url = `${BASE_URL}/api/events/is_assigned_to_customer?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}&customer_id=${customer.id}`;
  const result = fetchJsonSafe(url);
  if (!result.success) {
    section.addWidget(CardService.newDecoratedText().setText(text).setWrapText(true));
    return section;
  }

  const button = result.data.assigned
    ? CardService.newImageButton()
        .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/link_off_black_24dp.png")
        .setAltText("Unassign from Event")
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName("unassignCustomerFromEvent")
            .setParameters({
              customerId: String(customer.id),
              eventId: String(eventId)
            })
        )
    : CardService.newImageButton()
        .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/link_black_24dp.png")
        .setAltText("Assign to Event")
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName("assignCustomerToEvent")
            .setParameters({
              customerId: String(customer.id),
              eventId: String(eventId)
            })
        );
  
  section.addWidget(CardService.newDecoratedText().setText(text).setWrapText(true).setButton(button));

  return section;
}

function buildCustomerDetailSection(customer) {
  const section = CardService.newCardSection();

  section.addWidget(
    CardService.newDecoratedText()
      .setTopLabel("Email")
      .setText(customer.email || "N/A")
      .setWrapText(true)
  );

  section.addWidget(
    CardService.newDecoratedText()
      .setTopLabel("Phone")
      .setText(customer.tel || "N/A")
      .setWrapText(true)
  );

  section.addWidget(
    CardService.newDecoratedText()
      .setTopLabel("Location")
      .setText(customer.location || "N/A")
      .setWrapText(true)
  );

  if (customer.description) {
    section.addWidget(
      CardService.newDecoratedText()
        .setTopLabel("Description")
        .setText(customer.description)
        .setWrapText(true)
    );
  }

  if (customer.upcoming_events?.length > 0) {
    const eventsText = customer.upcoming_events
      .map(e => `${e.title}\n${new Date(e.start_time).toDateString()}`)
      .join("\n\n");

    section.addWidget(
      CardService.newDecoratedText()
        .setTopLabel("Upcoming Events")
        .setText(eventsText)
        .setWrapText(true)
    );
  }

  return section;
}

function buildAssignedCustomersSection(e) {
  const userEmail = getUserEmail_();
  const eventId = e.commonEventObject.parameters.eventId;
  const query = e?.commonEventObject?.parameters?.query || "";
  const url = `${BASE_URL}/api/events/assigned?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}&query=${encodeURIComponent(query)}`;
  const result = fetchJsonSafe(url);
  if (!result.success) return buildErrorCard(result.message);
  const customers = result.data;

  const section = CardService.newCardSection();
  if (customers.length === 0) {
    section.addWidget(
      CardService.newTextParagraph().setText("No customers assigned to this event.")
    );
  } else {
    customers.forEach(customer => {
      row = buildCustomerRow(customer, eventId, "assigned")
      section.addWidget(row);
    });
  }

  return section;
}

function buildAvailableCustomersSection(e) {
  const userEmail = getUserEmail_();
  const eventId = e.commonEventObject.parameters.eventId;
  const query = e?.commonEventObject?.parameters?.query || "";
  const url = `${BASE_URL}/api/events/available?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}&query=${encodeURIComponent(query)}`;
  const result = fetchJsonSafe(url);
  if (!result.success) return buildErrorCard(result.message);
  const customers = result.data;

  const section = CardService.newCardSection();
  if (customers.length === 0) {
    section.addWidget(
      CardService.newTextParagraph().setText("No available customers.")
    );
  } else {
      customers.forEach(customer => {
        row = buildCustomerRow(customer, eventId, "available")
        section.addWidget(row);
      });
  }

  return section;
}

function buildCustomerRow(customer, eventId, mode) {
  const name = `${customer.first_name} ${customer.last_name}`;
  const location = customer.location || "";

  const row = CardService.newKeyValue()
    .setContent(name)
    .setBottomLabel(location)
    .setOnClickAction(
      CardService.newAction()
        .setFunctionName("buildCustomerDetailCard")
        .setParameters({
          customerId: String(customer.id),
          eventId: String(eventId)
        })
    );

  if (eventId) {
    if (mode === "available") {
      const assignButton = CardService.newImageButton()
        .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/link_black_24dp.png")
        .setAltText("Assign to Event")
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName("assignCustomerToEvent")
            .setParameters({
              customerId: String(customer.id),
              eventId: String(eventId)
            })
        );
      row.setButton(assignButton);
    } else if (mode === "assigned") {
      const unassignButton = CardService.newImageButton()
        .setIconUrl("https://www.gstatic.com/images/icons/material/system/1x/link_off_black_24dp.png")
        .setAltText("Unassign from Event")
        .setOnClickAction(
          CardService.newAction()
            .setFunctionName("unassignCustomerFromEvent")
            .setParameters({
              customerId: String(customer.id),
              eventId: String(eventId)
            })
        );
      row.setButton(unassignButton);
    }
  }

  return row;
}

function assignCustomerToEvent(e) {
  const userEmail = getUserEmail_();
  const customerId = e.commonEventObject.parameters.customerId;
  const eventId = e.commonEventObject.parameters.eventId;
  const calendarId = getCalendarId_(e);
  const url = `${BASE_URL}/api/events/assign?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}`;
  const result = fetchJsonSafe(url, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({ customer_id: customerId, calendar_id: calendarId }),
    muteHttpExceptions: true
  });

  if (!result.success) {
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification().setText("Failed to assign customer."))
      .build();
  }

  const nav = CardService.newNavigation().updateCard(buildAssignUnassignCard(eventId, "assigned"));

  return CardService.newActionResponseBuilder().setNavigation(nav).build();
}

function unassignCustomerFromEvent(e) {
  const userEmail = getUserEmail_();
  const customerId = e.commonEventObject.parameters.customerId;
  const eventId = e.commonEventObject.parameters.eventId;
  const url = `${BASE_URL}/api/events/unassign?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}`;
  const result = fetchJsonSafe(url, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({ customer_id: customerId }),
    muteHttpExceptions: true
  });

  if (!result.success) {
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification().setText("Failed to unassign customer."))
      .build();
  }
  const checkUrl = `${BASE_URL}/api/events/is_assigned?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}`;
  const checkResult = fetchJsonSafe(checkUrl);

  if (!checkResult.success) {
    return CardService.newActionResponseBuilder()
      .setNotification(CardService.newNotification().setText("Unassigned, but failed to check status."))
      .build();
  }

  let updatedCard;
  if (checkResult.data.assigned) {
    updatedCard = buildAssignUnassignCard(eventId, "assigned");
  } else {
    updatedCard = buildCustomerListCard(eventId, "");
  }

  const nav = CardService.newNavigation().updateCard(updatedCard);

  return CardService.newActionResponseBuilder().setNavigation(nav).build();
}

function handleCreateCustomerSubmit(e) {
  const userEmail = getUserEmail_();
  const eventId = e?.commonEventObject?.parameters?.eventId || "";
  
  const data = {
    first_name: e.formInput.first_name,
    last_name: e.formInput.last_name,
    email: e.formInput.email,
    tel: e.formInput.tel,
    location: e.formInput.location,
    description: e.formInput.description
  };

  const result = fetchJsonSafe(
    `${BASE_URL}/api/customers?user_email=${encodeURIComponent(userEmail)}`,
    {
      method: "post",
      headers: { "Content-Type": "application/json" },
      payload: JSON.stringify(data),
      muteHttpExceptions: true
    }
  );

  if (!result.success) {
    return buildErrorCard("Failed to create customer.");
  }

  if (!eventId) {
    return buildCustomerListCard(eventId, "");
  }

  const checkUrl = `${BASE_URL}/api/events/is_assigned?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}`;
  const checkResult = fetchJsonSafe(checkUrl, { muteHttpExceptions: true });

  if (!checkResult.success) {
    return buildErrorCard("Failed to check event assignment.");
  }

  if (checkResult.data.assigned) {
    return buildAssignUnassignCard(eventId, "available");
  } else {
    return buildCustomerListCard(eventId, "");
  }
}

function handleEditCustomerSubmit(e) {
  const userEmail = getUserEmail_();
  const customerId = e.commonEventObject.parameters.customerId || "";
  const eventId = e?.commonEventObject?.parameters?.eventId || "";

  const data = {
    first_name: e.formInput.first_name,
    last_name: e.formInput.last_name,
    email: e.formInput.email,
    tel: e.formInput.tel,
    location: e.formInput.location,
    description: e.formInput.description
  };

  const result = fetchJsonSafe(
    `${BASE_URL}/api/customers/${customerId}?user_email=${encodeURIComponent(userEmail)}`,
    {
      method: "put",
      headers: { "Content-Type": "application/json" },
      payload: JSON.stringify(data),
      muteHttpExceptions: true
    }
  );
  if (!result.success) return buildErrorCard("Failed to update customer.");

  return buildCustomerDetailCard({
    commonEventObject: {
      parameters: {
        customerId: customerId,
        eventId: eventId
      }
    }
  });
}

function handleDeleteCustomer(e) {
  const userEmail = getUserEmail_();
  const customerId = e.parameters.customerId || "";
  const eventId = e?.commonEventObject?.parameters?.eventId || "";
  const url = `${BASE_URL}/api/customers/${customerId}?user_email=${encodeURIComponent(userEmail)}`;
  const result = fetchJsonSafe(url, {
    method: "delete",
    muteHttpExceptions: true
  });
  if (!result.success) return buildErrorCard("Failed to delete customer.");

  if (!eventId) {
    return buildCustomerListCard(eventId, "");
  }

  const checkUrl = `${BASE_URL}/api/events/is_assigned?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}`;
  const checkResult = fetchJsonSafe(checkUrl, { muteHttpExceptions: true });

  if (!checkResult.success) {
    return buildErrorCard("Failed to check event assignment.");
  }

  if (checkResult.data.assigned) {
    return buildAssignUnassignCard(eventId, "assigned");
  } else {
    return buildCustomerListCard(eventId, "");
  }
}

function handleSearchAction(e) {
  const eventId = e?.parameters?.eventId || "";
  const query = e?.formInput?.query || "";
  const source = e?.parameters?.source || "customer_list";

  if (source === "assigned_customers") {
    return buildAssignUnassignCard(eventId, "assigned", query);
  } else if (source === "available_customers") {
    return buildAssignUnassignCard(eventId, "available", query);
  } else {
    return buildCustomerListCard(eventId, query);
  }
}

function handleTabSwitch(e) {
  const eventId = e.parameters.eventId;
  const tab = e.parameters.tab;

  const nav = CardService.newNavigation().updateCard(buildAssignUnassignCard(eventId, tab));

  return CardService.newActionResponseBuilder()
    .setNavigation(nav)
    .build();
}

function handleInitialEntry(e) {
  const userEmail = getUserEmail_();
  const eventId = getEventId_(e);

  if (!eventId) {
    return buildCustomerListCard("", "");
  }

  const url = `${BASE_URL}/api/events/is_assigned?user_email=${encodeURIComponent(userEmail)}&google_event_id=${encodeURIComponent(eventId)}`;
  const result = fetchJsonSafe(url);

  if (!result.success) {
    return buildErrorCard("Failed to check assignment status.");
  }

  if (result.data.assigned) {
    return buildAssignUnassignCard(eventId, "assigned");
  } else {
    return buildCustomerListCard(eventId, "");
  }
}

function getUserEmail_() {
  return Session.getActiveUser().getEmail();
}

function getEventId_(e) {
  return e?.calendar?.id || null;
}

function getCalendarId_(e) {
  return e?.calendar?.calendarId || "primary";
}

function fetchJsonSafe(url, options = {}) {
  try {
    const response = UrlFetchApp.fetch(url, options);
    const code = response.getResponseCode();
    const content = response.getContentText();
    if (code >= 200 && code < 300) {
      return { success: true, data: JSON.parse(content) };
    } else {
      return { success: false, message: `API Error ${code}: ${content}` };
    }
  } catch (err) {
    return { success: false, message: "Network or server error." };
  }
}